"""
Handlungsempfehlungen – Frontend-Tests
=======================================
Testet das Recommendations-Feature auf dem Auswertungs-Tab:

  R1  Karte ist sichtbar wenn mind. 1 Frage Verbesserungspotenzial hat
  R2  Karte bleibt versteckt wenn alle Fragen mit "voll" beantwortet sind
  R3  Kategorien werden korrekt gruppiert (mind. 1 Kategorie sichtbar)
  R4  Kategorie-Header zeigt Anzahl der Empfehlungen als Badge
  R5  Klick auf Kategorie-Header klappt den Body ein und aus
  R6  Klick auf Gesamt-Toggle-Button klappt die gesamte Liste ein und aus

Hinweis: Tests laufen gegen den lokalen Flask-Server (http://127.0.0.1:5000).
"""

import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.project_page import ProjectPage
from conftest import TEST_USER

# Stichproben für niedrige Antworten (lösen Empfehlungen aus)
SAMPLE_LOW_ANSWERS = {
    "ts-1":  "nicht",   # Teststrategie – kein Treffer
    "tp-1":  "kaum",   # Testplanung – kaum Treffer
    "tme-1": "nicht",  # Testmetriken – kein Treffer
}


@pytest.fixture
def project_page(page: Page, base_url: str) -> ProjectPage:
    """Eingeloggter Testbenutzer, bereit für Projekterstellung."""
    LoginPage(page, base_url).login(TEST_USER["username"], TEST_USER["password"])
    return ProjectPage(page, base_url)


# ── R1: Karte sichtbar bei niedrigen Antworten ───────────────────────────────

def test_r1_recs_card_visible_with_low_answers(project_page: ProjectPage):
    pid = project_page.create_project("Pytest Recs - Low")
    project_page.goto(pid)

    for qid, val in SAMPLE_LOW_ANSWERS.items():
        project_page.answer_question(qid, val)

    project_page.open_auswertung_tab()

    expect(project_page.recs_card).to_be_visible()


# ── R2: Karte versteckt bei neuem Projekt ohne niedrige Antworten ─────────────

def test_r2_recs_card_hidden_when_no_low_answers(project_page: ProjectPage):
    """Neues Projekt, keine Fragen beantwortet → keine Empfehlungen → Karte versteckt."""
    pid = project_page.create_project("Pytest Recs - Empty")
    project_page.goto(pid)
    # Keine Antworten setzen – alle Fragen auf Standard ("---")
    project_page.open_auswertung_tab()

    # Karte darf nicht sichtbar sein (display:none)
    expect(project_page.recs_card).to_be_hidden()


# ── R3: Mind. 1 Kategorie-Abschnitt sichtbar ─────────────────────────────────

def test_r3_categories_rendered(project_page: ProjectPage):
    pid = project_page.create_project("Pytest Recs - Cats")
    project_page.goto(pid)

    for qid, val in SAMPLE_LOW_ANSWERS.items():
        project_page.answer_question(qid, val)

    project_page.open_auswertung_tab()

    assert project_page.category_count() >= 1, "Mindestens 1 Kategorie muss vorhanden sein"
    expect(project_page.cat_headers.first).to_be_visible()


# ── R4: Kategorie-Badge zeigt Empfehlungsanzahl ───────────────────────────────

def test_r4_category_count_badge(project_page: ProjectPage):
    pid = project_page.create_project("Pytest Recs - Badge")
    project_page.goto(pid)

    project_page.answer_question("ts-1", "nicht")
    project_page.open_auswertung_tab()

    # Badge-Text enthält "Empfehlung" (z.B. "1 Empfehlung" oder "9 Empfehlungen")
    first_header = project_page.cat_headers.first
    header_text = first_header.inner_text()
    assert "Empfehlung" in header_text, (
        f"Kategorie-Header enthält kein Zähl-Badge. Text: {header_text!r}"
    )


# ── R5: Kategorie einklappen / ausklappen ─────────────────────────────────────

def test_r5_category_toggle(project_page: ProjectPage):
    pid = project_page.create_project("Pytest Recs - Toggle Cat")
    project_page.goto(pid)

    for qid, val in SAMPLE_LOW_ANSWERS.items():
        project_page.answer_question(qid, val)

    project_page.open_auswertung_tab()

    # Body ist initial ausgeklappt
    assert project_page.is_cat_body_visible(0), "Kategorie-Body sollte initial sichtbar sein"

    # Einklappen
    project_page.toggle_category(0)
    assert not project_page.is_cat_body_visible(0), "Kategorie-Body sollte nach Klick versteckt sein"

    # Wieder ausklappen
    project_page.toggle_category(0)
    assert project_page.is_cat_body_visible(0), "Kategorie-Body sollte nach 2. Klick wieder sichtbar sein"


# ── R6: Gesamt-Toggle klappt gesamte Liste ein/aus ───────────────────────────

def test_r6_card_toggle(project_page: ProjectPage):
    pid = project_page.create_project("Pytest Recs - Toggle Card")
    project_page.goto(pid)

    for qid, val in SAMPLE_LOW_ANSWERS.items():
        project_page.answer_question(qid, val)

    project_page.open_auswertung_tab()

    # Liste initial sichtbar
    assert project_page.is_recs_list_visible(), "Empfehlungsliste sollte initial sichtbar sein"

    # Alles einklappen
    project_page.toggle_recs_card()
    assert not project_page.is_recs_list_visible(), "Liste sollte nach Toggle-Klick versteckt sein"

    # Wieder ausklappen
    project_page.toggle_recs_card()
    assert project_page.is_recs_list_visible(), "Liste sollte nach 2. Toggle-Klick wieder sichtbar sein"
