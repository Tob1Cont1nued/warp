"""
TC – Administration (/admin)
===============================
Gherkin-Umsetzung von tests/features/admin.feature.

Szenario → Testname:
  Admin-Seite zeigt alle UI-Elemente        → test_p1_admin_seite_elemente_sichtbar
  Admin legt einen neuen Benutzer an        → test_p2_admin_legt_benutzer_an
  Admin sperrt einen Benutzer               → test_p3_admin_sperrt_benutzer
  Admin kann eigenes Projekt anlegen        → test_p4_admin_kann_eigenes_projekt_anlegen
  Normaler Benutzer → /admin                → test_n1_normaler_benutzer_kann_admin_nicht_aufrufen
  Nicht eingeloggt → /admin                 → test_n2_nicht_eingeloggter_benutzer_wird_umgeleitet
"""

import re
import time

from playwright.sync_api import expect
from pytest_bdd import scenario, given, when, then

FEATURE = "../features/admin.feature"


def _unique_user() -> str:
    return f"_admin_test_{int(time.time() * 1000) % 100_000}"


# ---------------------------------------------------------------------------
# Szenario-Verknüpfungen
# ---------------------------------------------------------------------------

@scenario(FEATURE, "Admin-Seite zeigt alle UI-Elemente")
def test_p1_admin_seite_elemente_sichtbar():
    pass


@scenario(FEATURE, "Admin legt einen neuen Benutzer an")
def test_p2_admin_legt_benutzer_an():
    pass


@scenario(FEATURE, "Admin sperrt einen Benutzer")
def test_p3_admin_sperrt_benutzer():
    pass


@scenario(FEATURE, "Admin kann ein eigenes Projekt anlegen")
def test_p4_admin_kann_eigenes_projekt_anlegen():
    pass


@scenario(FEATURE, "Normaler Benutzer kann die Admin-Seite nicht aufrufen")
def test_n1_normaler_benutzer_kann_admin_nicht_aufrufen():
    pass


@scenario(FEATURE, "Nicht eingeloggter Benutzer wird zur Login-Seite umgeleitet")
def test_n2_nicht_eingeloggter_benutzer_wird_umgeleitet():
    pass


# ---------------------------------------------------------------------------
# Schritte
# ---------------------------------------------------------------------------

@then("sehe ich das Formular zum Anlegen eines neuen Benutzers")
def _see_form(admin_page):
    expect(admin_page.new_user_form).to_be_visible()
    expect(admin_page.username_input).to_be_visible()
    expect(admin_page.password_input).to_be_visible()
    expect(admin_page.submit_btn).to_be_visible()


@then("sehe ich mindestens eine Benutzerkarte in der Liste")
def _see_user_card(admin_page):
    expect(admin_page.user_cards.first).to_be_visible()


@when("ich einen neuen Benutzer mit Benutzername und Passwort anlege", target_fixture="new_username")
def _create_user(admin_page):
    username = _unique_user()
    admin_page.create_user(username, "testpasswort1")
    return username


@then("erscheint der neue Benutzer in der Benutzerliste")
def _see_new_user(admin_page, new_username):
    expect(admin_page.get_user_card(new_username)).to_be_visible()


@given("ich habe einen neuen Benutzer angelegt", target_fixture="new_username")
def _given_new_user(admin_page):
    username = _unique_user()
    admin_page.create_user(username, "testpasswort1")
    return username


@when("ich diesen Benutzer sperre")
def _lock_user(admin_page, new_username):
    admin_page.lock_user(new_username)


@then('zeigt die Benutzerkarte das Badge "gesperrt"')
def _see_locked_badge(admin_page, new_username):
    assert admin_page.is_user_locked(new_username)


@when('ich über "Neues Projekt" ein Projekt mit Namen anlege', target_fixture="current_page")
def _create_own_project(admin_page, base_url):
    admin_page.page.goto(f"{base_url}/project/new")
    admin_page.page.fill("#name", "AdminProjektTest")
    admin_page.page.click("button[type=submit]")
    return admin_page.page


@then("werde ich auf die neue Projektseite weitergeleitet")
def _on_new_project_page(current_page):
    expect(current_page).to_have_url(re.compile(r"/project/\d+$"))


@then("der Projektname ist auf der Seite sichtbar")
def _see_project_name(current_page):
    # Der Name taucht mehrfach auf (Sidebar-Liste + Titel etc.) - hier zählt
    # nur, dass er überhaupt sichtbar ist, nicht die exakte Anzahl.
    expect(current_page.locator("text=AdminProjektTest").first).to_be_visible()


@when("ich direkt die Admin-Seite aufrufe", target_fixture="direct_response")
def _goto_admin_directly(page, base_url):
    return page.goto(f"{base_url}/admin")


@then("bekomme ich den Status 403 Verboten")
def _status_403(direct_response):
    assert direct_response.status == 403


@then("werde ich zur Login-Seite umgeleitet")
def _redirected_login(page):
    expect(page).to_have_url(re.compile(r"/login"))
