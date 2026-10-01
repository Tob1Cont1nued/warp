"""
TC – Login (/login)
======================
Gherkin-Umsetzung von tests/features/login.feature. Nutzt dieselben Page
Objects (LoginPage, AdminPage) wie zuvor tests/test_login.py.

Szenario → Testname (für TEST_REGISTRY/Play-Buttons in testdokumentation.html):
  Login-Seite zeigt alle UI-Elemente        → test_p1_login_seite_elemente_sichtbar
  Admin-Login führt zum Dashboard           → test_p2_admin_login_leitet_auf_admin_weiter
  Benutzer-Login führt zum Dashboard        → test_p3_user_login_leitet_auf_projekt_weiter
  Falsches Passwort zeigt Fehlermeldung     → test_n1_falsches_passwort_zeigt_fehler
  Unbekannter Benutzername zeigt Fehler     → test_n2_unbekannter_benutzer_zeigt_fehler
  Gesperrter Benutzer bekommt Meldung       → test_n3_gesperrter_benutzer_zeigt_spezifische_meldung
"""

import time

from playwright.sync_api import expect
from pytest_bdd import scenario, given, when, then, parsers

from conftest import ADMIN
from pages.admin_page import AdminPage

FEATURE = "../features/login.feature"


def _unique_locked_user() -> str:
    return f"_pytest_locked_{int(time.time() * 1000) % 100_000}"


# ---------------------------------------------------------------------------
# Szenario-Verknüpfungen
# ---------------------------------------------------------------------------

@scenario(FEATURE, "Login-Seite zeigt alle UI-Elemente")
def test_p1_login_seite_elemente_sichtbar():
    pass


@scenario(FEATURE, "Admin-Login führt zum Dashboard")
def test_p2_admin_login_leitet_auf_admin_weiter():
    pass


@scenario(FEATURE, "Benutzer-Login führt zum Dashboard")
def test_p3_user_login_leitet_auf_projekt_weiter():
    pass


@scenario(FEATURE, "Falsches Passwort zeigt Fehlermeldung")
def test_n1_falsches_passwort_zeigt_fehler():
    pass


@scenario(FEATURE, "Unbekannter Benutzername zeigt Fehlermeldung")
def test_n2_unbekannter_benutzer_zeigt_fehler():
    pass


@scenario(FEATURE, "Gesperrter Benutzer bekommt spezifische Meldung")
def test_n3_gesperrter_benutzer_zeigt_spezifische_meldung():
    pass


# ---------------------------------------------------------------------------
# Schritte
# ---------------------------------------------------------------------------

@then("sehe ich das WARP-Logo mit Tagline")
def _see_logo(login_page):
    expect(login_page.brand_name).to_have_text("WARP")
    expect(login_page.brand_tagline).to_be_visible()


@then("sehe ich die Felder für Benutzername und Passwort")
def _see_fields(login_page):
    expect(login_page.username).to_be_visible()
    expect(login_page.password).to_be_visible()


@then("sehe ich den Anmelden-Button")
def _see_submit(login_page):
    expect(login_page.submit_btn).to_be_visible()


@then(parsers.parse('sehe ich den Link "{text}"'))
def _see_switch_link(login_page, text):
    expect(login_page.switch_link).to_be_visible()


@when("ich mich mit einem gültigen Benutzernamen aber falschem Passwort anmelde", target_fixture="current_page")
def _login_wrong_password(login_page):
    login_page.goto()
    login_page.username.fill(ADMIN["username"])
    login_page.password.fill("voellig_falsch")
    login_page.submit_btn.click()
    return login_page.page


@when("ich mich mit einem nicht existierenden Benutzernamen anmelde", target_fixture="current_page")
def _login_unknown_user(login_page):
    login_page.goto()
    login_page.username.fill("existiert_nicht_xyz")
    login_page.password.fill("egal")
    login_page.submit_btn.click()
    return login_page.page


@given("ein Admin hat ein Benutzerkonto angelegt und gesperrt", target_fixture="locked_user")
def _locked_user_setup(login_page, base_url):
    username = _unique_locked_user()
    password = "locked_pw_123"
    login_page.login(ADMIN["username"], ADMIN["password"])
    admin = AdminPage(login_page.page, base_url).goto()
    admin.create_user(username, password)
    admin.lock_user(username)
    login_page.page.goto(f"{base_url}/logout")
    login_page.page.wait_for_load_state("networkidle")
    return {"username": username, "password": password}


@when("ich mich mit dem gesperrten Konto anmelde", target_fixture="current_page")
def _login_locked_user(login_page, locked_user):
    login_page.username.fill(locked_user["username"])
    login_page.password.fill(locked_user["password"])
    login_page.submit_btn.click()
    return login_page.page
