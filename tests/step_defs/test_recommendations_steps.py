"""
TC – Handlungsempfehlungen (Auswertung-Tab)
==============================================
Gherkin-Umsetzung von tests/features/recommendations.feature. Echter
User-Flow: Login → Dashboard → "+" klicken → Projekt anlegen → Fragen
beantworten → Auswertung-Tab öffnen (wie zuvor tests/test_recommendations.py).

Szenario → Testname:
  Karte erscheint bei niedrigen Antworten     → test_r1_recs_card_visible_with_low_answers
  Karte bleibt ohne niedrige Antworten versteckt → test_r2_recs_card_hidden_without_low_answers
  Kategorien werden gruppiert                 → test_r3_categories_rendered
  Kategorie-Header zeigt Anzahl-Badge         → test_r4_category_count_badge
  Kategorie ein-/ausklappen                   → test_r5_category_toggle
  Gesamtliste ein-/ausklappen                 → test_r6_card_toggle
"""

from playwright.sync_api import expect
from pytest_bdd import scenario, given, when, then

from pages.project_page import DashboardPage, ProjectPage

FEATURE = "../features/recommendations.feature"

# Niedrige Antworten, die Empfehlungen in mehreren Kategorien auslösen
LOW_ANSWERS = {
    "ts-1":  "nicht",   # Teststrategie
    "tp-1":  "kaum",    # Testplanung
    "tme-1": "nicht",   # Testmetriken
}


# ---------------------------------------------------------------------------
# Szenario-Verknüpfungen
# ---------------------------------------------------------------------------

@scenario(FEATURE, "Empfehlungskarte erscheint bei niedrigen Antworten")
def test_r1_recs_card_visible_with_low_answers():
    pass


@scenario(FEATURE, "Empfehlungskarte bleibt ohne niedrige Antworten versteckt")
def test_r2_recs_card_hidden_without_low_answers():
    pass


@scenario(FEATURE, "Empfehlungen werden nach Kategorie gruppiert")
def test_r3_categories_rendered():
    pass


@scenario(FEATURE, "Kategorie-Überschrift zeigt die Anzahl der Empfehlungen")
def test_r4_category_count_badge():
    pass


@scenario(FEATURE, "Kategorie lässt sich ein- und wieder ausklappen")
def test_r5_category_toggle():
    pass


@scenario(FEATURE, "Gesamte Empfehlungsliste lässt sich ein- und wieder ausklappen")
def test_r6_card_toggle():
    pass


# ---------------------------------------------------------------------------
# Hintergrund (Background) – läuft vor jedem Szenario dieser Datei
# ---------------------------------------------------------------------------

@given("ich bin als normaler Benutzer eingeloggt und auf dem Dashboard", target_fixture="dashboard")
def _login_and_dashboard(page, base_url):
    from conftest import TEST_USER
    from pages.login_page import LoginPage
    LoginPage(page, base_url).login(TEST_USER["username"], TEST_USER["password"])
    expect(page.locator("h1", has_text="Dashboard")).to_be_visible()
    return DashboardPage(page)


@given('ich lege über "+" ein neues Projekt an', target_fixture="project_page")
def _create_project(dashboard):
    new_proj_page = dashboard.click_new_project()
    expect(new_proj_page.name_input).to_be_visible()
    return new_proj_page.create("Pytest Recs – Playwright")


# ---------------------------------------------------------------------------
# Schritte
# ---------------------------------------------------------------------------

@when("ich Fragen mit niedriger Bewertung in mehreren Kategorien beantworte")
def _answer_low(project_page: ProjectPage):
    for qid, val in LOW_ANSWERS.items():
        project_page.answer_question(qid, val)


@when('ich eine Frage mit "Trifft nicht zu" beantworte')
def _answer_one_low(project_page: ProjectPage):
    project_page.answer_question("ts-1", "nicht")


@when("ich keine Fragen beantworte")
def _answer_none():
    pass


@when("ich den Auswertung-Tab öffne")
def _open_auswertung(project_page: ProjectPage):
    project_page.click_auswertung_tab()


@then("sehe ich die Handlungsempfehlungen-Karte")
def _see_recs_card(project_page: ProjectPage):
    expect(project_page.recs_card).to_be_visible()


@then("sehe ich die Handlungsempfehlungen-Karte nicht")
def _recs_card_hidden(project_page: ProjectPage):
    expect(project_page.recs_card).to_be_hidden()


@then("sehe ich mindestens eine Kategorie-Überschrift")
def _see_category_header(project_page: ProjectPage):
    assert project_page.category_count() >= 1, "Mindestens 1 Kategorie muss vorhanden sein"
    expect(project_page.cat_headers.first).to_be_visible()


@then('enthält die erste Kategorie-Überschrift das Wort "Empfehlung"')
def _category_header_has_badge(project_page: ProjectPage):
    header_text = project_page.cat_headers.first.inner_text()
    assert "Empfehlung" in header_text, (
        f"Kategorie-Header enthält kein Anzahl-Badge. Gefundener Text: {header_text!r}"
    )


@then("ist der Inhalt der ersten Kategorie sichtbar")
def _category_body_visible(project_page: ProjectPage):
    assert project_page.is_cat_body_visible(0), "Kategorie-Body sollte sichtbar sein"


@then("ist der Inhalt der ersten Kategorie nicht mehr sichtbar")
def _category_body_hidden(project_page: ProjectPage):
    assert not project_page.is_cat_body_visible(0), "Kategorie-Body sollte eingeklappt sein"


@then("ist der Inhalt der ersten Kategorie wieder sichtbar")
def _category_body_visible_again(project_page: ProjectPage):
    assert project_page.is_cat_body_visible(0), "Kategorie-Body sollte wieder ausgeklappt sein"


@when("ich auf die erste Kategorie-Überschrift klicke")
def _toggle_category(project_page: ProjectPage):
    project_page.toggle_category(0)


@when("ich erneut auf die erste Kategorie-Überschrift klicke")
def _toggle_category_again(project_page: ProjectPage):
    project_page.toggle_category(0)


@then("ist die Empfehlungsliste sichtbar")
def _recs_list_visible(project_page: ProjectPage):
    assert project_page.is_recs_list_visible(), "Empfehlungsliste sollte sichtbar sein"


@then("ist die Empfehlungsliste nicht mehr sichtbar")
def _recs_list_hidden(project_page: ProjectPage):
    assert not project_page.is_recs_list_visible(), "Empfehlungsliste sollte eingeklappt sein"


@then("ist die Empfehlungsliste wieder sichtbar")
def _recs_list_visible_again(project_page: ProjectPage):
    assert project_page.is_recs_list_visible(), "Empfehlungsliste sollte wieder sichtbar sein"


@when("ich auf den Gesamt-Toggle-Button klicke")
def _toggle_card(project_page: ProjectPage):
    project_page.toggle_recs_card()


@when("ich erneut auf den Gesamt-Toggle-Button klicke")
def _toggle_card_again(project_page: ProjectPage):
    project_page.toggle_recs_card()
