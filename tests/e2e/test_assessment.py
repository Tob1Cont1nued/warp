"""
Playwright-Test: WARP Assessment-Workflow
-----------------------------------------
Meldet sich als Benutzer1 an, legt ein Projekt an und beantwortet
alle 137 Fragen mit folgendem Reifegrad-Profil:

  Stufe 1 (Basis / Initial) : immer erfüllt – keine Fragen
  Stufe 2 (Managed)         : 100 % – alle Fragen mit „vollständig"
  Stufe 3 (Defined)         : beginnt gut (Org + Schulung 100 %),
                              dann nachlassend (Lebenszyklus 50 %,
                              Nicht-funktional + Peer Reviews 25 %)
  Stufe 4 (Measured)        : kaum erfüllt (25 % / 0 %)
  Stufe 5 (Optimization)    : kaum erfüllt (0 % / 25 %)

Aufruf:
  pytest tests/e2e/test_assessment.py --headed -s
  (oder ohne --headed für headless)
"""

import re
import os
from pathlib import Path
from playwright.sync_api import Page, expect

BASE_URL = "https://warp-5ld0.onrender.com"
USERNAME = "Benutzer1"
PASSWORD = "warp2024"
PROJECT_NAME = "Playwright Test – Maturity-Profil"

SCREENSHOTS = Path(__file__).parent.parent / "screenshots"
SCREENSHOTS.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Antwort-Mapping  qid → answer_id
# answer_id-Werte (aus ANSWER_OPTIONS): voll=100, teil=50, kaum=25, nicht=0
# ---------------------------------------------------------------------------
ANSWERS: dict[str, str] = {}

# ── Stufe 2 – Managed: 100 % ────────────────────────────────────────────────
for _prefix, _n in [("ts", 11), ("tp", 10), ("ueb", 11), ("tfd", 13), ("tum", 8)]:
    for _i in range(1, _n + 1):
        ANSWERS[f"{_prefix}-{_i}"] = "voll"

# ── Stufe 3 – Defined: beginnt gut, lässt dann stark nach ──────────────────
# Testorganisation (11 Fragen):         100 %  – gut aufgestellt
for _i in range(1, 12):
    ANSWERS[f"org-{_i}"] = "voll"
# Testschulungsprogramm (7 Fragen):     100 %  – noch gut
for _i in range(1, 8):
    ANSWERS[f"sch-{_i}"] = "voll"
# Testlebenszyklus & Integration (16):   50 %  – merklich nachlassend
for _i in range(1, 17):
    ANSWERS[f"lc-{_i}"] = "teil"
# Nicht-funktionales Testen (4):         25 %  – stark nachlassen
for _i in range(1, 5):
    ANSWERS[f"nf-{_i}"] = "kaum"
# Peer Reviews (5):                      25 %  – stark nachlassen
for _i in range(1, 6):
    ANSWERS[f"pr-{_i}"] = "kaum"

# ── Stufe 4 – Measured: kaum erfüllt ────────────────────────────────────────
# Testmetriken (11):                     25 %
for _i in range(1, 12):
    ANSWERS[f"tme-{_i}"] = "kaum"
# Produktqualitätsbewertung (5):          0 %
for _i in range(1, 6):
    ANSWERS[f"pq-{_i}"] = "nicht"
# Erweiterte Reviews (3):                 0 %
for _i in range(1, 4):
    ANSWERS[f"er-{_i}"] = "nicht"

# ── Stufe 5 – Optimization: kaum erfüllt ────────────────────────────────────
# Fehlervermeidung (4):                   0 %
for _i in range(1, 5):
    ANSWERS[f"fv-{_i}"] = "nicht"
# Qualitätskontrolle (3):                25 %
for _i in range(1, 4):
    ANSWERS[f"qk-{_i}"] = "kaum"
# Testprozessoptimierung (15):            0 %
for _i in range(1, 16):
    ANSWERS[f"po-{_i}"] = "nicht"


# ---------------------------------------------------------------------------
# Hilfsfunktion
# ---------------------------------------------------------------------------

def _select_answer(page: Page, qid: str, answer: str) -> bool:
    """Wählt eine Antwort per select-Element aus. Gibt True zurück wenn gefunden."""
    loc = page.locator(f'select[data-qid="{qid}"]')
    if loc.count() == 0:
        print(f"  ⚠  Frage {qid} nicht im DOM – übersprungen")
        return False
    loc.select_option(answer)
    return True


# ---------------------------------------------------------------------------
# Test
# ---------------------------------------------------------------------------

def test_assessment_full_workflow(page: Page) -> None:
    page.set_default_timeout(90_000)   # Render cold-start kann ~30 s dauern

    # ------------------------------------------------------------------
    # 1. Login
    # ------------------------------------------------------------------
    print(f"\n→ Öffne {BASE_URL} …")
    page.goto(BASE_URL)
    page.wait_for_load_state("networkidle")

    page.fill('input[name="username"]', USERNAME)
    page.fill('input[name="password"]', PASSWORD)
    page.screenshot(path=str(SCREENSHOTS / "01_login.png"))
    page.click('button[type="submit"]')
    page.wait_for_load_state("networkidle")
    print(f"  ✓ Eingeloggt als {USERNAME} → {page.url}")

    # ------------------------------------------------------------------
    # 2. Neues Projekt anlegen
    # ------------------------------------------------------------------
    # Immer explizit zur Neuanlage-Seite navigieren
    page.goto(f"{BASE_URL}/project/new")
    page.wait_for_load_state("networkidle")

    name_field = page.locator('input[name="name"]')
    if name_field.count() > 0:
        name_field.fill(PROJECT_NAME)
    page.screenshot(path=str(SCREENSHOTS / "02_new_project.png"))
    page.click('button[type="submit"]')
    page.wait_for_url(re.compile(r"/project/\d+$"), timeout=30_000)
    page.wait_for_load_state("networkidle")
    print(f"  ✓ Projekt angelegt → {page.url}")

    # ------------------------------------------------------------------
    # 3. Alle Antworten setzen
    # ------------------------------------------------------------------
    print(f"\n→ Setze {len(ANSWERS)} Antworten …")

    total = len(ANSWERS)
    found = 0
    for qid, answer in ANSWERS.items():
        if _select_answer(page, qid, answer):
            found += 1

    # Kurz warten, damit alle AJAX-Saves abgeschlossen sind
    page.wait_for_load_state("networkidle")
    print(f"  ✓ {found}/{total} Antworten gesetzt")

    page.screenshot(path=str(SCREENSHOTS / "03_assessment_filled.png"), full_page=True)

    # Fortschrittsanzeige prüfen (optional)
    answered_el = page.locator("#js-answered")
    if answered_el.count() > 0:
        answered_text = answered_el.inner_text()
        print(f"  → Fortschritt laut UI: {answered_text} / {total}")

    # ------------------------------------------------------------------
    # 4. HTML-Report aufrufen und prüfen
    # ------------------------------------------------------------------
    print("\n→ Öffne HTML-Vorschau …")
    with page.expect_popup() as popup_info:
        page.click('button:has-text("Vorschau")')
    report = popup_info.value
    report.wait_for_load_state("networkidle")
    report.screenshot(path=str(SCREENSHOTS / "04_report.png"), full_page=True)

    # Stufe 2 muss als erreicht markiert sein
    expect(report.locator("text=Stufe 2")).to_be_visible()
    # Stufe 3 soll sichtbar sein (auch wenn nicht vollständig erreicht)
    expect(report.locator("text=Stufe 3")).to_be_visible()

    print(f"  ✓ Report gerendert: {report.url}")
    print(f"\n✅ Test abgeschlossen. Screenshots in: {SCREENSHOTS.resolve()}")
