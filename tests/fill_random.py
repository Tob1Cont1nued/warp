"""
WARP Tool – Playwright-Automatisierung
=======================================
Beantwortet alle Fragen des Fragenkatalogs zufällig und öffnet
den HTML-Report-Preview im Browser.

Voraussetzungen (einmalig):
    pip install playwright
    playwright install chromium

Verwendung:
    python tests/fill_random.py                        # zufällig
    python tests/fill_random.py --bias high            # überwiegend hohe Scores  (gut → grüner Report)
    python tests/fill_random.py --bias medium          # ausgewogen
    python tests/fill_random.py --bias low             # überwiegend niedrige Scores
    python tests/fill_random.py --seed 42              # reproduzierbare Zufallswahl
    python tests/fill_random.py --project "Kunde X" --owner "Max Mustermann"
    python tests/fill_random.py --username myuser --password mypassword

Hinweis: Admin-Konten können keine Projekte anlegen. Benutze einen regulären User-Account.
"""

import argparse
import random
import subprocess
import sys
import time
from pathlib import Path

BASE_URL = "http://127.0.0.1:5000"
ANSWER_IDS = ["voll", "teil", "kaum", "nicht"]

# Gewichtung je Bias-Profil (voll / teil / kaum / nicht)
BIAS_WEIGHTS: dict[str, list[int]] = {
    "random": [25, 25, 25, 25],
    "high":   [60, 25, 10,  5],
    "medium": [30, 35, 25, 10],
    "low":    [ 5, 10, 25, 60],
}

ROOT = Path(__file__).parent.parent


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="WARP – Fragenbogen zufällig ausfüllen",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--bias", choices=list(BIAS_WEIGHTS), default="random",
                   help="Antwort-Tendenz (default: random)")
    p.add_argument("--seed", type=int, default=None,
                   help="Zufalls-Seed für reproduzierbare Ergebnisse")
    p.add_argument("--project", default="Automatisierter Test-Run",
                   help="Projektname im Report")
    p.add_argument("--owner", default="WARP Playwright Bot",
                   help="Verantwortliche/r im Report")
    p.add_argument("--username", default="fill_bot",
                   help="Login-Benutzername (default: fill_bot)")
    p.add_argument("--password", default="warp_fill_2024",
                   help="Login-Passwort (default: warp_fill_2024)")
    return p.parse_args()


# ---------------------------------------------------------------------------
# Flask-Verwaltung
# ---------------------------------------------------------------------------

def flask_running(port: int = 5000) -> bool:
    """Prüft per HTTP ob der Server tatsächlich antwortet (nicht nur TCP-Port offen)."""
    try:
        import urllib.request
        urllib.request.urlopen(f"http://127.0.0.1:{port}/login", timeout=2)
        return True
    except Exception:
        return False


def start_flask() -> subprocess.Popen:
    proc = subprocess.Popen(
        [sys.executable, "run.py"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print("Flask startet", end="", flush=True)
    for _ in range(30):
        time.sleep(0.5)
        print(".", end="", flush=True)
        if flask_running():
            print(" bereit.")
            return proc
    proc.kill()
    sys.exit("\n[FEHLER] Flask-Server konnte nicht gestartet werden.")


# ---------------------------------------------------------------------------
# Hauptlogik
# ---------------------------------------------------------------------------

def main() -> None:
    args = parse_args()
    rng = random.Random(args.seed)
    weights = BIAS_WEIGHTS[args.bias]

    # Playwright-Import prüfen
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit(
            "[FEHLER] Playwright nicht installiert.\n"
            "Bitte ausführen:\n"
            "  pip install playwright\n"
            "  playwright install chromium"
        )

    # Flask starten (falls nicht schon aktiv)
    flask_proc = None
    if flask_running():
        print("Flask läuft bereits auf Port 5000.")
    else:
        flask_proc = start_flask()

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=False)
            context = browser.new_context(viewport={"width": 1440, "height": 900})
            page = context.new_page()

            # ----------------------------------------------------------------
            # Seite laden + Login (falls erforderlich)
            # ----------------------------------------------------------------
            print(f"Lade {BASE_URL} …")
            page.goto(BASE_URL)
            page.wait_for_load_state("networkidle")

            if "/login" in page.url:
                print(f"Login als '{args.username}' …")
                page.fill("#username", args.username)
                page.fill("#password", args.password)
                page.click("button[type=submit]")
                page.wait_for_load_state("networkidle")

                # Login fehlgeschlagen → Benutzer noch nicht registriert
                if "/login" in page.url:
                    print(f"  → Benutzer nicht gefunden, registriere '{args.username}' …")
                    page.goto(f"{BASE_URL}/register")
                    page.fill("#username", args.username)
                    page.fill("#password", args.password)
                    page.fill("#password2", args.password)
                    page.click("button[type=submit]")
                    page.wait_for_load_state("networkidle")

                if "/admin" in page.url:
                    sys.exit(
                        "[FEHLER] Admin-Konten können keine Projekte anlegen.\n"
                        "Bitte einen regulären Benutzer angeben:\n"
                        "  python tests/fill_random.py --username myuser --password mypassword"
                    )

            # ----------------------------------------------------------------
            # Neues Projekt anlegen falls noch keins vorhanden
            # ----------------------------------------------------------------
            if "/project/new" in page.url:
                print(f"Lege Projekt '{args.project}' an …")
                page.fill("#name", args.project)
                page.click("button[type=submit]")
                page.wait_for_load_state("networkidle")

            # ----------------------------------------------------------------
            # Projektinformationen
            # ----------------------------------------------------------------
            page.fill("#project_name", args.project)
            page.fill("#project_owner", args.owner)

            # ----------------------------------------------------------------
            # Alle Fragen befüllen
            # ----------------------------------------------------------------
            selects = page.query_selector_all("select.js-answer")
            total = len(selects)
            print(f"{total} Fragen gefunden. Bias: {args.bias}"
                  + (f", Seed: {args.seed}" if args.seed is not None else "") + " …")

            for i, sel in enumerate(selects, 1):
                choice = rng.choices(ANSWER_IDS, weights=weights)[0]
                sel.select_option(choice)
                # Fortschrittsbalken in der Konsole
                if i % 20 == 0 or i == total:
                    bar = "#" * (i * 30 // total)
                    print(f"\r  [{bar:<30}] {i}/{total}", end="", flush=True)

            print()  # Zeilenumbruch nach Fortschrittsbalken

            # Gegencheck: Counter im DOM
            answered_text = page.locator("#js-answered").text_content()
            print(f"DOM-Zähler: {answered_text} / {total} beantwortet")

            # ----------------------------------------------------------------
            # HTML-Vorschau öffnen (Button öffnet neuen Tab via formtarget=_blank)
            # ----------------------------------------------------------------
            print("Öffne HTML-Vorschau …")
            with context.expect_page() as new_page_info:
                page.locator('form[action*="report/html"] button[type=submit]').click()

            report_page = new_page_info.value
            report_page.wait_for_load_state("networkidle")
            print(f"Report geladen: {report_page.url}")

            print("\nTab 1: Ausgefüllter Fragenkatalog  |  Tab 2: Report-Vorschau")
            print("Browser offen – schließen Sie ihn oder drücken Sie Strg+C zum Beenden.")
            try:
                while browser.is_connected():
                    time.sleep(0.5)
            except KeyboardInterrupt:
                pass

            browser.close()

    finally:
        if flask_proc is not None:
            flask_proc.terminate()
            print("Flask-Server gestoppt.")


if __name__ == "__main__":
    main()
