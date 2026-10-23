"""
TC-KV – Kinderveranstaltungen-Finder (/veranstaltungen)
=======================================================
Claude (anthropic-Modul) und der Ortsdienst (Nominatim) sind gefakt – kein Netzwerk,
kein API-Guthaben nötig.

TC-KV-01  Seite ohne Login                          → Weiterleitung zum Login
TC-KV-02  Seite mit Login                           → 200, Suchformular
TC-KV-03  Suche ohne Ort                            → 400
TC-KV-04  Unbekannter Ort                           → 404 mit Hinweis
TC-KV-05  Suche läuft bis "done": Entfernung berechnet, sortiert, zu weit Entferntes
          aussortiert, unsichere Links entfernt, Websuche + Modell im Request
TC-KV-06  Gleiche Suche erneut                      → sofort aus dem Cache, kein 2. API-Call
TC-KV-07  Abgelehnte Anfrage (refusal)              → Status "error" mit Meldung
TC-KV-08  Login mit next=/veranstaltungen           → landet auf der Seite;
          next=//fremde-seite                       → landet NICHT extern
"""

import json
import sys
import time
import types

import pytest

import app.veranstaltungen as kv
from tests.unit.conftest import _ensure_user

CENTER = {"name": "Münster", "lat": 51.9629, "lon": 7.6250}

ANSWER = {"veranstaltungen": [
    {"name": "Kindertheater Fernes", "kategorie": "kultur", "wetter": "indoor", "lat": 51.9629, "lon": 7.9,
     "quelle": "https://example.org/theater", "kostenlos": False},
    {"name": "Allwetterzoo", "kategorie": "zoo", "wetter": "beides", "lat": 51.9480, "lon": 7.5870,
     "quelle": "javascript:alert(1)", "kostenlos": False},
    {"name": "Viel zu weit weg", "kategorie": "event", "lat": 53.55, "lon": 9.99},
    {"name": "", "kategorie": "event"},
]}


class _FakeBetaMessages:
    def __init__(self, recorder):
        self.recorder = recorder

    def create(self, **kwargs):
        self.recorder["calls"].append(kwargs)
        if self.recorder.get("refuse"):
            return types.SimpleNamespace(stop_reason="refusal", content=[], model=kwargs["model"])
        text = "Hier die Ergebnisse:\n```json\n" + json.dumps(ANSWER) + "\n```"
        return types.SimpleNamespace(
            stop_reason="end_turn", model=kwargs["model"],
            content=[types.SimpleNamespace(type="text", text=text)],
        )


@pytest.fixture
def fake_claude(monkeypatch):
    recorder = {"calls": []}

    class _Client:
        def __init__(self, api_key=None, timeout=None):
            self.beta = types.SimpleNamespace(messages=_FakeBetaMessages(recorder))

    fake = types.ModuleType("anthropic")
    fake.Anthropic = _Client
    monkeypatch.setitem(sys.modules, "anthropic", fake)
    monkeypatch.setattr(kv, "geocode", lambda q: dict(CENTER) if q.lower().startswith("münster") else None)
    kv._cache.clear()
    kv._jobs.clear()
    return recorder


def _wait(user_client, job_id, timeout=5.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        d = user_client.get(f"/veranstaltungen/suche/{job_id}").get_json()
        if d["status"] != "running":
            return d
        time.sleep(0.05)
    pytest.fail("Suche wurde nicht fertig")


class TestKinderveranstaltungen:
    def test_tc_kv_01_ohne_login_weiterleitung(self, client):
        r = client.get("/veranstaltungen")
        assert r.status_code == 302
        assert "/login" in r.headers["Location"]

    def test_tc_kv_02_seite_mit_login(self, user_client):
        r = user_client.get("/veranstaltungen")
        assert r.status_code == 200
        assert "Kinderveranstaltungen finden".encode() in r.data
        assert b'id="geoButton"' in r.data

    def test_tc_kv_03_suche_ohne_ort(self, user_client, fake_claude):
        r = user_client.post("/veranstaltungen/suche", json={"radius": 15})
        assert r.status_code == 400

    def test_tc_kv_04_unbekannter_ort(self, user_client, fake_claude):
        r = user_client.post("/veranstaltungen/suche", json={"name": "Nirgendwo"})
        assert r.status_code == 404
        assert "nicht gefunden" in r.get_json()["error"]

    def test_tc_kv_05_suche_liefert_aufbereitete_ergebnisse(self, user_client, fake_claude):
        r = user_client.post("/veranstaltungen/suche", json={"name": "Münster", "radius": 25, "date": "2026-10-24"})
        assert r.status_code == 200
        start = r.get_json()
        assert start["place"]["lat"] == CENTER["lat"]

        d = _wait(user_client, start["job"])
        assert d["status"] == "done"
        names = [e["name"] for e in d["events"]]
        # sortiert nach Entfernung, Hamburg (>200 km) und namenloser Eintrag aussortiert
        assert names == ["Allwetterzoo", "Kindertheater Fernes"]
        zoo, theater = d["events"]
        assert 0 < zoo["entfernung"] < theater["entfernung"] <= 25
        assert zoo["quelle"] == ""                     # javascript:-Link verworfen
        assert theater["quelle"] == "https://example.org/theater"

        call = fake_claude["calls"][0]
        assert call["model"] == "claude-opus-5-5"
        assert call["tools"][0]["type"] == "web_search_20260209"
        prompt = call["messages"][0]["content"]
        assert "Samstag, 24.10.2026" in prompt and "25 km" in prompt

    def test_tc_kv_06_gleiche_suche_aus_cache(self, user_client, fake_claude):
        body = {"name": "Münster", "radius": 15}
        first = user_client.post("/veranstaltungen/suche", json=body).get_json()
        _wait(user_client, first["job"])
        second = user_client.post("/veranstaltungen/suche", json=body).get_json()
        d = user_client.get(f"/veranstaltungen/suche/{second['job']}").get_json()
        assert d["status"] == "done" and d["cached"] is True
        assert len(fake_claude["calls"]) == 1

    def test_tc_kv_07_ablehnung_wird_gemeldet(self, user_client, fake_claude):
        fake_claude["refuse"] = True
        start = user_client.post("/veranstaltungen/suche", json={"name": "Münster"}).get_json()
        d = _wait(user_client, start["job"])
        assert d["status"] == "error"
        assert "abgelehnt" in d["error"]

    def test_tc_kv_08_login_weiterleitung_nur_lokal(self, app):
        _ensure_user(app, "_kv_user", "kv_pw_12345")
        c = app.test_client()
        r = c.post("/login?next=/veranstaltungen", data={"username": "_kv_user", "password": "kv_pw_12345"})
        assert r.status_code == 302 and r.headers["Location"].endswith("/veranstaltungen")

        c2 = app.test_client()
        r2 = c2.post("/login?next=//fremde-seite.example", data={"username": "_kv_user", "password": "kv_pw_12345"})
        assert r2.status_code == 302
        assert "fremde-seite" not in r2.headers["Location"]
