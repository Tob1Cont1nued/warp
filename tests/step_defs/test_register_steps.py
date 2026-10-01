"""
TC – Registrierung (/register)
=================================
Gherkin-Umsetzung von tests/features/register.feature.

Szenario → Testname:
  Registrierungs-Seite zeigt alle UI-Elemente   → test_p1_register_seite_elemente_sichtbar
  Neuer Benutzer landet auf dem Dashboard       → test_p2_neuer_benutzer_wird_angelegt_und_weitergeleitet
  Link "Bereits registriert" → Login-Seite      → test_p3_anmelden_link_navigiert_zur_login_seite
  Bereits vergebener Benutzername               → test_n1_doppelter_benutzername_zeigt_fehler
  Nicht übereinstimmende Passwörter             → test_n2_passwort_mismatch_zeigt_fehler
  Zu kurzes Passwort                            → test_n3_passwort_zu_kurz_zeigt_fehler
"""

import time

from playwright.sync_api import expect
from pytest_bdd import scenario, given, when, then

from conftest import TEST_USER

FEATURE = "../features/register.feature"


def _unique_user() -> str:
    return f"_pytest_reg_{int(time.time() * 1000) % 100_000}"


# ---------------------------------------------------------------------------
# Szenario-Verknüpfungen
# ---------------------------------------------------------------------------

@scenario(FEATURE, "Registrierungs-Seite zeigt alle UI-Elemente")
def test_p1_register_seite_elemente_sichtbar():
    pass


@scenario(FEATURE, "Neuer Benutzer landet nach Registrierung auf dem Dashboard")
def test_p2_neuer_benutzer_wird_angelegt_und_weitergeleitet():
    pass


@scenario(FEATURE, 'Link "Bereits registriert" führt zur Login-Seite')
def test_p3_anmelden_link_navigiert_zur_login_seite():
    pass


@scenario(FEATURE, "Bereits vergebener Benutzername zeigt Fehlermeldung")
def test_n1_doppelter_benutzername_zeigt_fehler():
    pass


@scenario(FEATURE, "Nicht übereinstimmende Passwörter zeigen Fehlermeldung")
def test_n2_passwort_mismatch_zeigt_fehler():
    pass


@scenario(FEATURE, "Zu kurzes Passwort zeigt Fehlermeldung")
def test_n3_passwort_zu_kurz_zeigt_fehler():
    pass


# ---------------------------------------------------------------------------
# Schritte
# ---------------------------------------------------------------------------

@when("ich die Registrierungs-Seite öffne", target_fixture="current_page")
def _open_register(register_page):
    register_page.goto()
    return register_page.page


@then("sehe ich das WARP-Logo auf der Registrierungs-Seite")
def _see_logo(register_page):
    expect(register_page.brand_name).to_have_text("WARP")


@then("sehe ich die Felder Benutzername, Anzeigename, Passwort und Passwort-Bestätigung")
def _see_fields(register_page):
    expect(register_page.username).to_be_visible()
    expect(register_page.display_name).to_be_visible()
    expect(register_page.password).to_be_visible()
    expect(register_page.password2).to_be_visible()


@then("sehe ich den Registrieren-Button")
def _see_submit(register_page):
    expect(register_page.submit_btn).to_be_visible()


@then('sehe ich den Link "Bereits registriert? Anmelden"')
def _see_switch_link(register_page):
    expect(register_page.switch_link).to_be_visible()


@when("ich mich mit einem neuen, eindeutigen Benutzernamen registriere", target_fixture="current_page")
def _register_new_user(register_page):
    register_page.register(_unique_user(), "sicher123", display_name="Playwright User")
    return register_page.page


@when('ich auf "Bereits registriert? Anmelden" klicke', target_fixture="current_page")
def _click_switch_link(register_page):
    register_page.switch_link.click()
    return register_page.page


@then("lande ich auf der Login-Seite")
def _on_login_page(current_page, base_url):
    expect(current_page).to_have_url(f"{base_url}/login")


@when("ich mich mit einem bereits vergebenen Benutzernamen registriere", target_fixture="current_page")
def _register_duplicate(register_page):
    register_page.register(TEST_USER["username"], "irgendetwas123")
    return register_page.page


@when("ich mich mit zwei unterschiedlichen Passwörtern registriere", target_fixture="current_page")
def _register_mismatch(register_page):
    register_page.register(_unique_user(), "passwort1", password2="passwort2")
    return register_page.page


@when("ich mich mit einem zu kurzen Passwort registriere", target_fixture="current_page")
def _register_short_pw(register_page):
    register_page.register(_unique_user(), "abc")
    return register_page.page
