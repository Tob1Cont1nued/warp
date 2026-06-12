"""
Fragenkatalog-Seite (/project/<id>) – Oberflächentests (Page Object Model)
===========================================================================
Positiv:
  P1  Alle UI-Elemente auf der Questionnaire-Seite sind sichtbar
  P2  Antwort wird gespeichert (AJAX auto-save) – Selektion bleibt nach Reload
  P3  Download-Buttons für Vorlagen sind vorhanden und verlinkt

Negativ:
  N1  Nicht eingeloggter Benutzer wird zur Login-Seite umgeleitet
  N2  Benutzer kann nicht auf ein fremdes Projekt zugreifen (403)
  N3  Zugriff auf nicht existierende Projekt-ID liefert 403
"""

import re
from playwright.sync_api import Page, expect
from conftest import TEST_USER, TEST_USER2
from pages.login_page import LoginPage
from pages.questionnaire_page import QuestionnairePage


# ── Positiv-Tests ────────────────────────────────────────────────────────────

def test_p1_questionnaire_elemente_sichtbar(user_page):
    expect(user_page.brand_name).to_have_text("WARP")
    expect(user_page.brand_tagline).to_be_visible()
    expect(user_page.projects_sidebar).to_be_visible()
    expect(user_page.new_project_btn).to_be_visible()
    expect(user_page.logout_link).to_be_visible()
    expect(user_page.answer_selects.first).to_be_visible()
    expect(user_page.note_textareas.first).to_be_visible()
    expect(user_page.progress_bar).to_be_visible()
    expect(user_page.auswertung_section).to_be_visible()


def test_p2_antwort_wird_nach_reload_gespeichert(user_page):
    value = user_page.select_first_answer()
    user_page.wait_for_autosave()
    user_page.page.reload()
    user_page.page.wait_for_load_state("networkidle")
    assert user_page.answer_selects.first.input_value() == value


def test_p3_download_buttons_vorhanden_und_verlinkt(user_page):
    btns = user_page.download_buttons.all()
    assert len(btns) == 3, f"Erwartet 3 Download-Buttons, gefunden: {len(btns)}"
    for btn in btns:
        href = btn.get_attribute("href") or ""
        assert href.endswith(".docx"), f"Kein .docx-Link: {href}"


# ── Negativ-Tests ────────────────────────────────────────────────────────────

def test_n1_nicht_eingeloggter_benutzer_wird_umgeleitet(page: Page, base_url):
    QuestionnairePage(page, base_url).goto(1)
    expect(page).to_have_url(re.compile(r"/login"))


def test_n2_fremdes_projekt_liefert_403(user_page, base_url, setup_test_users):
    """USER2 kann nicht auf ein Projekt von USER1 zugreifen."""
    match = re.search(r"/project/(\d+)", user_page.page.url)
    assert match, "Konnte Projekt-ID von USER1 nicht ermitteln"
    project_id = match.group(1)

    # Ausloggen und als USER2 einloggen
    user_page.page.goto(f"{base_url}/logout")
    user_page.page.wait_for_load_state("networkidle")
    LoginPage(user_page.page, base_url).login(TEST_USER2["username"], TEST_USER2["password"])

    response = user_page.page.goto(f"{base_url}/project/{project_id}")
    assert response.status == 403


def test_n3_nicht_existierende_projekt_id_liefert_403(user_page, base_url):
    response = user_page.page.goto(f"{base_url}/project/999999")
    assert response.status == 403
