"""
Kinderveranstaltungen-Finder
============================
Eigenständige Seite innerhalb der WARP-App (fachlich unabhängig vom Assessment):
sucht für einen Ort, ein Datum und einen Umkreis aktuelle Kinderveranstaltungen
und Ausflugsziele. Die Recherche übernimmt Claude mit Websuche - serverseitig,
damit der API-Key nie im Browser landet.

Ablauf:
  GET  /veranstaltungen                 Seite (Login erforderlich)
  GET  /veranstaltungen/ort             Ort <-> Koordinaten (OpenStreetMap/Nominatim)
  POST /veranstaltungen/suche           startet eine Recherche im Hintergrund -> {job}
  GET  /veranstaltungen/suche/<job>     Status/Ergebnis der Recherche (Polling)

Die Recherche dauert typischerweise 30-90 s - länger als ein vorgeschalteter
Proxy einen Request offen hält. Darum Hintergrund-Thread + Polling, wie bei der
KI-Dokumentgenerierung. Wie dort setzt der In-Memory-Jobspeicher einen einzelnen
Gunicorn-Worker voraus (siehe Procfile).
"""
from __future__ import annotations

import datetime as dt
import json
import math
import os
import re
import threading
import time
import uuid
from collections import OrderedDict

import requests
from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required

from . import limiter

bp = Blueprint("veranstaltungen", __name__)

MODEL = "claude-opus-5-5"

CATEGORIES = OrderedDict([
    ("zoo", "🦁 Zoo & Tiere"),
    ("museum", "🏛️ Museen"),
    ("spielplatz", "🎢 Spielplätze & Indoor-Spielplätze"),
    ("sport", "⛹️ Sport & Bäder"),
    ("kultur", "🎭 Theater, Kino & Kultur"),
    ("natur", "🌲 Natur & Wanderungen"),
    ("event", "🎪 Events, Feste & Märkte"),
])
WEATHER = {"indoor": "drinnen (wetterunabhängig)", "outdoor": "draußen"}

NOMINATIM = "https://nominatim.openstreetmap.org"
# Nominatim verlangt einen aussagekräftigen User-Agent (Nutzungsrichtlinie).
NOMINATIM_HEADERS = {"User-Agent": "WARP-Kinderveranstaltungen/1.0 (warp-5ld0.onrender.com)"}

_jobs: dict[str, dict] = {}
_cache: "OrderedDict[tuple, tuple[float, dict]]" = OrderedDict()
_lock = threading.Lock()
JOB_TTL = 3600          # s - abgeschlossene Jobs werden danach verworfen
CACHE_TTL = 6 * 3600    # s - gleiche Suche innerhalb von 6 h kommt aus dem Cache
CACHE_MAX = 100


# ── Geodaten ──────────────────────────────────────────────────────────────

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return round(r * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)), 1)


def _place_name(address: dict) -> str | None:
    city = address.get("city") or address.get("town") or address.get("village") or address.get("municipality")
    part = address.get("suburb") or address.get("city_district") or address.get("quarter")
    if city and part and part != city:
        # OSM führt manche Stadtteile schon mit Stadtnamen ("Münster-Hiltrup").
        return part if city.lower() in part.lower() else f"{city}-{part}"
    return city or part


def geocode(query: str) -> dict | None:
    """Ort/Stadtteil/PLZ -> {name, lat, lon} oder None."""
    r = requests.get(
        f"{NOMINATIM}/search",
        params={"q": query, "format": "jsonv2", "limit": 1, "countrycodes": "de",
                "addressdetails": 1, "accept-language": "de"},
        headers=NOMINATIM_HEADERS, timeout=8,
    )
    r.raise_for_status()
    hits = r.json()
    if not hits:
        return None
    h = hits[0]
    name = _place_name(h.get("address") or {}) or h.get("name") or query
    return {"name": name, "lat": float(h["lat"]), "lon": float(h["lon"])}


def reverse_geocode(lat: float, lon: float) -> str | None:
    r = requests.get(
        f"{NOMINATIM}/reverse",
        params={"lat": lat, "lon": lon, "format": "jsonv2", "zoom": 14, "accept-language": "de"},
        headers=NOMINATIM_HEADERS, timeout=8,
    )
    r.raise_for_status()
    return _place_name(r.json().get("address") or {})


def _valid_coords(lat, lon) -> bool:
    return isinstance(lat, (int, float)) and isinstance(lon, (int, float)) and abs(lat) <= 90 and abs(lon) <= 180


# ── Recherche mit Claude ──────────────────────────────────────────────────

SYSTEM_PROMPT = """Du bist ein Familien-Concierge für Deutschland. Du recherchierst mit der \
Websuche aktuelle Veranstaltungen und Ausflugsziele für Kinder (ca. 2-12 Jahre) und ihre Eltern.

Regeln:
- Nur Angebote, die du in der Websuche tatsächlich gefunden hast - nichts erfinden. \
Lieber weniger, dafür belastbare Treffer.
- Zeitgebundene Veranstaltungen (Kindertheater, Feste, Märkte, Workshops, Ferienaktionen) \
haben Vorrang, wenn sie in den gesuchten Zeitraum fallen. Dauerhafte Ausflugsziele \
(Zoo, Museum, Indoor-Spielplatz, Schwimmbad) ergänzen, wenn sie an dem Tag geöffnet sind.
- Prüfe Datum und Öffnungszeiten gegen den gesuchten Zeitraum. Bist du unsicher, sag es \
im Feld "hinweis".
- Alle Angebote müssen im angegebenen Umkreis um den Mittelpunkt liegen.
- Gib für jedes Angebot die Koordinaten des Veranstaltungsorts so genau wie möglich an.
- Schreibe auf Deutsch, knapp und konkret.

Antworte am Ende AUSSCHLIESSLICH mit einem JSON-Objekt in einem ```json-Codeblock, \
ohne weiteren Text danach:
{"veranstaltungen": [{
  "name": "...",
  "kategorie": "zoo|museum|spielplatz|sport|kultur|natur|event",
  "wetter": "indoor|outdoor|beides",
  "wann": "konkreter Termin oder Öffnungszeiten am gesuchten Tag",
  "kosten": "z.B. 'Kinder 5 €, Erwachsene 8 €' oder 'kostenlos'",
  "kostenlos": true|false,
  "alter": "z.B. 'ab 4 Jahren' oder ''",
  "adresse": "Straße Hausnummer, PLZ Ort",
  "lat": 51.96, "lon": 7.62,
  "beschreibung": "1-2 Sätze",
  "tipp": "praktischer Tipp für Eltern oder ''",
  "hinweis": "Unsicherheiten, z.B. 'Termin bitte prüfen', sonst ''",
  "quelle": "URL der Seite, auf der du es gefunden hast"
}]}"""


_WEEKDAYS = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]


def _de_date(d: dt.date) -> str:
    # Nicht strftime('%A'): auf dem Server ist keine deutsche Locale gesetzt.
    return f"{_WEEKDAYS[d.weekday()]}, {d.strftime('%d.%m.%Y')}"


def _build_prompt(p: dict) -> str:
    if p["date"]:
        when = f"am {_de_date(dt.date.fromisoformat(p['date']))}"
    else:
        when = f"in den nächsten 7 Tagen (heute ist {_de_date(dt.date.today())})"
    lines = [
        f"Suche Kinderveranstaltungen und Ausflugsziele {when}.",
        f"Mittelpunkt: {p['name']} (Koordinaten {p['lat']:.4f}, {p['lon']:.4f}).",
        f"Umkreis: höchstens {p['radius']} km.",
    ]
    if p["category"]:
        lines.append(f"Nur Kategorie: {CATEGORIES[p['category']]}.")
    if p["weather"]:
        lines.append(f"Nur Angebote {WEATHER[p['weather']]}.")
    lines.append("Liefere 5 bis 12 Treffer, nach Entfernung sortiert.")
    return "\n".join(lines)


def _extract_json(text: str) -> dict:
    m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.S)
    raw = m.group(1) if m else text[text.find("{"): text.rfind("}") + 1]
    return json.loads(raw)


def _clean_event(e: dict, center: dict) -> dict | None:
    if not isinstance(e, dict) or not str(e.get("name") or "").strip():
        return None

    def s(key: str, limit: int = 400) -> str:
        v = e.get(key)
        return str(v).strip()[:limit] if v is not None else ""

    quelle = s("quelle", 500)
    if not quelle.startswith(("http://", "https://")):
        quelle = ""
    lat, lon = e.get("lat"), e.get("lon")
    distance = haversine_km(center["lat"], center["lon"], lat, lon) if _valid_coords(lat, lon) else None
    kategorie = s("kategorie", 20)
    wetter = s("wetter", 10)
    return {
        "name": s("name", 160),
        "kategorie": kategorie if kategorie in CATEGORIES else "event",
        "wetter": wetter if wetter in ("indoor", "outdoor", "beides") else "beides",
        "wann": s("wann"), "kosten": s("kosten", 160), "kostenlos": bool(e.get("kostenlos")),
        "alter": s("alter", 80), "adresse": s("adresse", 200),
        "beschreibung": s("beschreibung", 600), "tipp": s("tipp"), "hinweis": s("hinweis"),
        "quelle": quelle, "entfernung": distance,
    }


def research(p: dict) -> dict:
    """Führt die Recherche aus (blockierend) und liefert {events, model}."""
    import anthropic  # erst hier - Tests ersetzen das Modul (siehe test_veranstaltungen.py)

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY ist auf dem Server nicht gesetzt.")
    client = anthropic.Anthropic(api_key=api_key, timeout=300)

    tools = [{
        "type": "web_search_20260209",
        "name": "web_search",
        "max_uses": 8,  # begrenzt Dauer und Kosten einer Suche
        "user_location": {"type": "approximate", "city": p["name"][:60], "country": "DE",
                          "timezone": "Europe/Berlin"},
    }]
    messages = [{"role": "user", "content": _build_prompt(p)}]

    response = None
    for _ in range(4):  # pause_turn: lange Websuche-Runden werden fortgesetzt
        response = client.beta.messages.create(
            model=MODEL,
            max_tokens=16000,
            system=SYSTEM_PROMPT,
            messages=messages,
            tools=tools,
            output_config={"effort": "medium"},
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
        )
        if response.stop_reason != "pause_turn":
            break
        messages = messages[:1] + [{"role": "assistant", "content": response.content}]

    if response.stop_reason == "refusal":
        raise RuntimeError("Die Anfrage wurde abgelehnt. Bitte die Suche anders formulieren.")
    text = "".join(b.text for b in response.content if getattr(b, "type", None) == "text")
    try:
        data = _extract_json(text)
    except (ValueError, json.JSONDecodeError):
        raise RuntimeError("Die Antwort konnte nicht ausgewertet werden. Bitte noch einmal suchen.")

    center = {"lat": p["lat"], "lon": p["lon"]}
    events = [ev for ev in (_clean_event(e, center) for e in data.get("veranstaltungen") or []) if ev]
    # Angebote mit bekannter Entfernung deutlich außerhalb des Umkreises aussortieren
    # (etwas Toleranz für ungenaue Koordinaten).
    events = [ev for ev in events if ev["entfernung"] is None or ev["entfernung"] <= p["radius"] * 1.3]
    events.sort(key=lambda ev: (ev["entfernung"] is None, ev["entfernung"] or 0))
    return {"events": events, "model": getattr(response, "model", MODEL)}


def _run_job(job_id: str, p: dict, cache_key: tuple) -> None:
    try:
        result = research(p)
        with _lock:
            _cache[cache_key] = (time.time(), result)
            _cache.move_to_end(cache_key)
            while len(_cache) > CACHE_MAX:
                _cache.popitem(last=False)
            _jobs[job_id].update(status="done", result=result, finished=time.time())
    except Exception as exc:  # Fehler landen beim Nutzer statt im Nichts
        msg = str(exc) if isinstance(exc, RuntimeError) else "Die Recherche ist fehlgeschlagen. Bitte später erneut versuchen."
        with _lock:
            _jobs[job_id].update(status="error", error=msg, finished=time.time())


# ── Routen ────────────────────────────────────────────────────────────────

@bp.route("/veranstaltungen")
@login_required
def page():
    return render_template("veranstaltungen.html", categories=CATEGORIES)


@bp.route("/veranstaltungen/ort")
@login_required
def place():
    """?q=<Ort/PLZ> -> Koordinaten, oder ?lat=&lon= -> Ortsname."""
    try:
        if request.args.get("q"):
            hit = geocode(request.args["q"].strip()[:120])
            if not hit:
                return jsonify({"ok": False, "error": "Ort nicht gefunden"}), 404
            return jsonify({"ok": True, **hit})
        lat, lon = float(request.args["lat"]), float(request.args["lon"])
        if not _valid_coords(lat, lon):
            raise ValueError
        return jsonify({"ok": True, "name": reverse_geocode(lat, lon) or "Mein Standort", "lat": lat, "lon": lon})
    except (KeyError, ValueError):
        return jsonify({"ok": False, "error": "q oder lat/lon angeben"}), 400
    except requests.RequestException:
        return jsonify({"ok": False, "error": "Ortsdienst nicht erreichbar"}), 502


def _user_key() -> str:
    return f"user:{current_user.get_id()}"


@bp.route("/veranstaltungen/suche", methods=["POST"])
@login_required
@limiter.limit("20 per hour", key_func=_user_key)
def start_search():
    data = request.get_json(silent=True) or {}
    try:
        radius = int(data.get("radius") or 15)
    except (TypeError, ValueError):
        radius = 15
    radius = max(1, min(radius, 100))
    date = (data.get("date") or "").strip()
    if date:
        try:
            dt.date.fromisoformat(date)
        except ValueError:
            return jsonify({"ok": False, "error": "Ungültiges Datum"}), 400
    category = data.get("category") or ""
    weather = data.get("weather") or ""
    if category not in CATEGORIES:
        category = ""
    if weather not in WEATHER:
        weather = ""

    lat, lon = data.get("lat"), data.get("lon")
    name = str(data.get("name") or "").strip()[:120]
    if not _valid_coords(lat, lon):
        if not name:
            return jsonify({"ok": False, "error": "Bitte einen Ort angeben"}), 400
        try:
            hit = geocode(name)
        except requests.RequestException:
            return jsonify({"ok": False, "error": "Ortsdienst nicht erreichbar"}), 502
        if not hit:
            return jsonify({"ok": False, "error": f"„{name}“ wurde nicht gefunden"}), 404
        name, lat, lon = hit["name"], hit["lat"], hit["lon"]

    p = {"name": name or "Mein Standort", "lat": float(lat), "lon": float(lon), "radius": radius,
         "date": date, "category": category, "weather": weather}
    cache_key = (round(p["lat"], 2), round(p["lon"], 2), radius, date or dt.date.today().isoformat(),
                 category, weather)
    job_id = uuid.uuid4().hex
    now = time.time()
    with _lock:
        for jid in [j for j, v in _jobs.items() if now - v["created"] > JOB_TTL]:
            del _jobs[jid]
        cached = _cache.get(cache_key)
        if cached and now - cached[0] < CACHE_TTL:
            _jobs[job_id] = {"status": "done", "result": cached[1], "created": now, "place": p, "cached": True}
            return jsonify({"ok": True, "job": job_id, "place": p})
        _jobs[job_id] = {"status": "running", "created": now, "place": p}
    threading.Thread(target=_run_job, args=(job_id, p, cache_key), daemon=True).start()
    return jsonify({"ok": True, "job": job_id, "place": p})


@bp.route("/veranstaltungen/suche/<job_id>")
@login_required
def search_status(job_id: str):
    with _lock:
        job = _jobs.get(job_id)
        if job is None:
            return jsonify({"ok": False, "error": "Suche nicht gefunden"}), 404
        out = {"ok": True, "status": job["status"], "place": job["place"],
               "elapsed": round(time.time() - job["created"])}
        if job["status"] == "done":
            out.update(events=job["result"]["events"], cached=job.get("cached", False))
        elif job["status"] == "error":
            out["error"] = job["error"]
    return jsonify(out)
