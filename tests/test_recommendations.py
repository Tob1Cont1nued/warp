"""
Handlungsempfehlungen – Frontend-Tests (echter User-Flow)
==========================================================
Jeder Test simuliert exakt das Verhalten eines echten Users:
  Login → Dashboard → '+' klicken → Projekt anlegen →
  Fragen beantworten → 'Auswertung'-Tab klicken → Empfehlungen prüfen

  R1  Karte sichtbar wenn mind. 1 Frage Verbesserungspotenzial hat
  R2  Karte versteckt bei neuem Projekt (keine niedrigen Antworten)
  R3  Kategorien korrekt gruppiert (mind. 1 Kategorie sichtbar)
  R4  Kategorie-Header zeigt Anzahl-Badge ("… Empfehlung(en)")
  R5  Klick auf Kategorie-Header klappt Body ein und wieder aus
  R6  Gesamt-Toggle-Button klappt gesamte Liste ein und wieder aus
"""

from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.project_page import DashboardPage, ProjectPage
from conftest import TEST_USER

# Niedrige Antworten die Empfehlungen auslösen
LOW_ANSWERS = {
    "ts-1":  "nicht",   # Teststrategie
    "tp-1":  "kaum",    # Testplanung
    "tme-1": "nicht",   # Testmetriken
}


def _login_and_dashboard(page: Page, base_url: str) -> DashboardPage:
    """Login als Testbenutzer und auf dem Dashboard ankommen."""
    LoginPage(page, base_url).login(TEST_USER["username"], TEST_USER["password"])
    expect(page.locator("h1", has_text="Dashboard")).to_be_visible()
    return DashboardPage(page)


def _setup_project_with_answers(page: Page, base_url: str,
                                 name: str, answers: dict) -> ProjectPage:
    """
    Kompletter User-Flow:
    Login → Dashboard → '+' klicken → Projekt anlegen →
    Antworten setzen → Auswertungs-Tab öffnen.
    Gibt die ProjectPage zurück (Auswertung bereits aktiv).
    """
    dashboard = _login_and_dashboard(page, base_url)

    # User klickt '+' in der Sidebar
    new_proj_page = dashboard.click_new_project()
    expect(new_proj_page.name_input).to_be_visible()

    # User trägt Projektnamen ein und klickt 'Erstellen'
    project_page = new_proj_page.create(name)

    # User beantwortet Fragen über die Dropdown-Menüs
    for qid, val in answers.items():
        project_page.answer_question(qid, val)

    # User klickt den 'Auswertung'-Tab
    project_page.click_auswertung_tab()
    return project_page


# ── R1: Karte sichtbar bei niedrigen Antworten ───────────────────────────────

def test_r1_recs_card_visible_with_low_answers(page: Page, base_url: str):
    project = _setup_project_with_answers(page, base_url,
                                          "Pytest R1 – Low Answers", LOW_ANSWERS)
    expect(project.recs_card).to_be_visible()


# ── R2: Karte versteckt ohne niedrige Antworten ───────────────────────────────

def test_r2_recs_card_hidden_without_low_answers(page: Page, base_url: str):
    """Neues Projekt, keine Antworten → Karte bleibt versteckt."""
    dashboard = _login_and_dashboard(page, base_url)
    new_proj_page = dashboard.click_new_project()
    project = new_proj_page.create("Pytest R2 – No Answers")

    # User klickt direkt 'Auswertung', ohne eine Frage zu beantworten
    project.click_auswertung_tab()
    expect(project.recs_card).to_be_hidden()


# ── R3: Kategorien werden angezeigt ──────────────────────────────────────────

def test_r3_categories_rendered(page: Page, base_url: str):
    project = _setup_project_with_answers(page, base_url,
                                          "Pytest R3 – Categories", LOW_ANSWERS)
    assert project.category_count() >= 1, "Mindestens 1 Kategorie muss vorhanden sein"
    expect(project.cat_headers.first).to_be_visible()


# ── R4: Badge zeigt Empfehlungsanzahl ────────────────────────────────────────

def test_r4_category_count_badge(page: Page, base_url: str):
    project = _setup_project_with_answers(page, base_url,
                                          "Pytest R4 – Badge",
                                          {"ts-1": "nicht"})
    header_text = project.cat_headers.first.inner_text()
    assert "Empfehlung" in header_text, (
        f"Kategorie-Header enthält kein Anzahl-Badge. Gefundener Text: {header_text!r}"
    )


# ── R5: Kategorie einklappen / ausklappen ─────────────────────────────────────

def test_r5_category_toggle(page: Page, base_url: str):
    project = _setup_project_with_answers(page, base_url,
                                          "Pytest R5 – Category Toggle", LOW_ANSWERS)

    # Body initial sichtbar
    assert project.is_cat_body_visible(0), "Kategorie-Body sollte initial ausgeklappt sein"

    # User klickt Kategorie-Header → eingeklappt
    project.toggle_category(0)
    assert not project.is_cat_body_visible(0), "Kategorie-Body sollte nach Klick eingeklappt sein"

    # User klickt nochmal → wieder ausgeklappt
    project.toggle_category(0)
    assert project.is_cat_body_visible(0), "Kategorie-Body sollte nach 2. Klick wieder sichtbar sein"


# ── R6: Gesamt-Toggle klappt alle Empfehlungen ein/aus ───────────────────────

def test_r6_card_toggle(page: Page, base_url: str):
    project = _setup_project_with_answers(page, base_url,
                                          "Pytest R6 – Card Toggle", LOW_ANSWERS)

    # Empfehlungsliste initial sichtbar
    assert project.is_recs_list_visible(), "Empfehlungsliste sollte initial sichtbar sein"

    # User klickt den Pfeil-Button oben rechts → alles eingeklappt
    project.toggle_recs_card()
    assert not project.is_recs_list_visible(), "Liste sollte nach Toggle eingeklappt sein"

    # User klickt nochmal → wieder ausgeklappt
    project.toggle_recs_card()
    assert project.is_recs_list_visible(), "Liste sollte nach 2. Toggle wieder sichtbar sein"
