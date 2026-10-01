"""
TC – Fragenkatalog (/project/<id>)
=====================================
Gherkin-Umsetzung von tests/features/questionnaire.feature.

Szenario → Testname:
  UI-Elemente sichtbar                 → test_p1_questionnaire_elemente_sichtbar
  Antwort bleibt nach Reload erhalten  → test_p2_antwort_wird_nach_reload_gespeichert
  Vorlagen-Downloads verlinkt          → test_p3_download_buttons_vorhanden_und_verlinkt
  Nicht eingeloggt → Redirect          → test_n1_nicht_eingeloggter_benutzer_wird_umgeleitet
  Fremdes Projekt → 403                → test_n2_fremdes_projekt_liefert_403
  Nicht existente ID → 404             → test_n3_nicht_existierende_projekt_id_liefert_404
"""

import re

from playwright.sync_api import expect
from pytest_bdd import scenario, given, when, then

from conftest import TEST_USER2
from pages.login_page import LoginPage
from pages.questionnaire_page import QuestionnairePage

FEATURE = "../features/questionnaire.feature"


# ---------------------------------------------------------------------------
# Szenario-Verknüpfungen
# ---------------------------------------------------------------------------

@scenario(FEATURE, "Fragenkatalog-Seite zeigt alle UI-Elemente")
def test_p1_questionnaire_elemente_sichtbar():
    pass


@scenario(FEATURE, "Antwort bleibt nach Neuladen der Seite erhalten")
def test_p2_antwort_wird_nach_reload_gespeichert():
    pass


@scenario(FEATURE, "Vorlagen-Downloads sind vorhanden und verlinkt")
def test_p3_download_buttons_vorhanden_und_verlinkt():
    pass


@scenario(FEATURE, "Nicht eingeloggter Benutzer wird zur Login-Seite umgeleitet")
def test_n1_nicht_eingeloggter_benutzer_wird_umgeleitet():
    pass


@scenario(FEATURE, "Benutzer kann nicht auf ein fremdes Projekt zugreifen")
def test_n2_fremdes_projekt_liefert_403():
    pass


@scenario(FEATURE, "Nicht existierende Projekt-ID liefert 404")
def test_n3_nicht_existierende_projekt_id_liefert_404():
    pass


# ---------------------------------------------------------------------------
# Schritte
# ---------------------------------------------------------------------------

@then("sehe ich die Projekt-Sidebar mit \"Neues Projekt\"-Button")
def _see_sidebar(user_page):
    expect(user_page.brand_name).to_have_text("WARP")
    expect(user_page.brand_tagline).to_be_visible()
    expect(user_page.projects_sidebar).to_be_visible()
    expect(user_page.new_project_btn).to_be_visible()


@then("sehe ich im Profil-Dropdown den Abmelden-Link")
def _see_logout_in_dropdown(user_page):
    expect(user_page.profile_btn).to_be_visible()
    user_page.profile_btn.click()
    expect(user_page.logout_link).to_be_visible()
    user_page.profile_btn.click()  # Dropdown wieder schließen


@then("sehe ich mindestens eine Antwort-Auswahl und ein Notizfeld")
def _see_answer_and_note(user_page):
    expect(user_page.answer_selects.first).to_be_visible()
    expect(user_page.note_textareas.first).to_be_visible()


@then("sehe ich den Fortschrittsbalken und den Auswertung-Tab")
def _see_progress_and_tab(user_page):
    expect(user_page.progress_bar).to_be_visible()
    expect(user_page.auswertung_tab_btn).to_be_visible()


@when("ich die erste Frage beantworte", target_fixture="chosen_answer")
def _answer_first_question(user_page):
    value = user_page.select_first_answer()
    user_page.wait_for_autosave()
    return value


@when("ich die Seite neu lade")
def _reload(user_page):
    user_page.page.reload()
    user_page.page.wait_for_load_state("networkidle")


@then("ist dieselbe Antwort weiterhin ausgewählt")
def _answer_persisted(user_page, chosen_answer):
    assert user_page.answer_selects.first.input_value() == chosen_answer


@when("ich die Vorlagen-Seite öffne")
def _open_vorlagen(user_page, base_url):
    user_page.page.goto(f"{base_url}/vorlagen")


@then("sehe ich genau 3 Download-Buttons, die auf .docx-Dateien verlinken")
def _see_download_buttons(user_page):
    btns = user_page.page.locator(".dok-btn-dl").all()
    assert len(btns) == 3, f"Erwartet 3 Download-Buttons, gefunden: {len(btns)}"
    for btn in btns:
        href = btn.get_attribute("href") or ""
        assert href.endswith(".docx"), f"Kein .docx-Link: {href}"


@when("ich direkt ein Projekt über seine URL aufrufe", target_fixture="current_page")
def _goto_project_directly(page, base_url):
    QuestionnairePage(page, base_url).goto(1)
    return page


@when("sich ein anderer Benutzer anmeldet und mein Projekt über die URL aufruft", target_fixture="direct_response")
def _other_user_access(user_page, base_url):
    match = re.search(r"/project/(\d+)", user_page.page.url)
    assert match, "Konnte Projekt-ID nicht ermitteln"
    project_id = match.group(1)

    user_page.page.goto(f"{base_url}/logout")
    user_page.page.wait_for_load_state("networkidle")
    LoginPage(user_page.page, base_url).login(TEST_USER2["username"], TEST_USER2["password"])

    return user_page.page.goto(f"{base_url}/project/{project_id}")


@then("bekommt dieser Benutzer den Status 403 Verboten")
def _status_403(direct_response):
    assert direct_response.status == 403


@when("ich ein Projekt mit einer nicht existierenden ID aufrufe", target_fixture="direct_response")
def _goto_nonexistent_project(user_page, base_url):
    return user_page.page.goto(f"{base_url}/project/999999")


@then("bekomme ich den Status 404 Nicht gefunden")
def _status_404(direct_response):
    assert direct_response.status == 404
