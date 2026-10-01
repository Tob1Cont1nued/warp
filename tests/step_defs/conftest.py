"""
Gemeinsame Gherkin-Schritte für alle Feature-Dateien unter tests/features/.

Liegt bewusst als conftest.py (nicht als normales Modul), damit pytest-bdd
die @given/@when/@then-Fixtures automatisch allen Szenario-Dateien in diesem
Verzeichnis zur Verfügung stellt, ohne dass jede Datei sie einzeln
importieren muss. Seitenspezifische Schritte stehen weiterhin in der
jeweiligen tests/step_defs/test_<bereich>_steps.py.

Nutzt dieselben Page Objects und Fixtures (login_page, admin_page, user_page,
base_url, ADMIN, TEST_USER, ...) wie die vorherigen tests/test_<bereich>.py -
die sind nicht verschwunden, sondern leben jetzt als Schritt-Implementierung.
"""

import re
import sys
from pathlib import Path

from playwright.sync_api import expect
from pytest_bdd import given, when, then, parsers

# tests/ in sys.path aufnehmen, damit "from pages.xxx import ..." klappt
# (dieselbe Zeile wie in tests/conftest.py, hier zusätzlich nötig weil
# pytest-bdd die Schritte unabhängig vom Testmodul auflöst).
sys.path.insert(0, str(Path(__file__).parent.parent))

from conftest import ADMIN, TEST_USER, TEST_USER2  # noqa: E402
from pages.login_page import LoginPage  # noqa: E402


# ---------------------------------------------------------------------------
# Angenommen (Given)
# ---------------------------------------------------------------------------

@given("ich bin nicht eingeloggt")
def _not_logged_in():
    """Reine Dokumentation der Vorbedingung - die page-Fixture ist ohnehin
    unangemeldet, bis ein Login-Schritt folgt."""
    pass


@given("ich bin als Admin eingeloggt", target_fixture="current_page")
def _given_admin_logged_in(admin_page):
    return admin_page.page


@given("ich bin als Admin eingeloggt und auf dem Dashboard", target_fixture="current_page")
def _given_admin_logged_in_dashboard(page, base_url):
    LoginPage(page, base_url).login(ADMIN["username"], ADMIN["password"])
    page.goto(f"{base_url}/dashboard")
    return page


@given("ich bin als normaler Benutzer eingeloggt", target_fixture="current_page")
def _given_user_logged_in(page, base_url):
    LoginPage(page, base_url).login(TEST_USER["username"], TEST_USER["password"])
    return page


@given("ich bin als Benutzer mit einem eigenen Projekt eingeloggt", target_fixture="current_page")
def _given_user_with_project(user_page):
    return user_page.page


# ---------------------------------------------------------------------------
# Wenn (When)
# ---------------------------------------------------------------------------

@when("ich die Login-Seite öffne", target_fixture="current_page")
def _open_login(login_page):
    login_page.goto()
    return login_page.page


@when("ich mich mit einem Admin-Konto anmelde", target_fixture="current_page")
def _login_as_admin(login_page):
    login_page.login(ADMIN["username"], ADMIN["password"])
    return login_page.page


@when("ich mich mit einem normalen Benutzerkonto anmelde", target_fixture="current_page")
def _login_as_user(login_page):
    login_page.login(TEST_USER["username"], TEST_USER["password"])
    return login_page.page


# ---------------------------------------------------------------------------
# Dann (Then)
# ---------------------------------------------------------------------------

@then("werde ich auf das Dashboard weitergeleitet")
def _then_on_dashboard(current_page, base_url):
    expect(current_page).to_have_url(f"{base_url}/dashboard")


@then("sehe ich eine Fehlermeldung")
def _then_see_error(current_page):
    expect(current_page.locator(".login-error")).to_be_visible()


@then(parsers.parse('enthält die Fehlermeldung den Text "{text}"'))
def _then_error_contains(current_page, text):
    expect(current_page.locator(".login-error")).to_contain_text(text)


@then("ich bleibe auf der Login-Seite")
def _then_still_on_login(current_page):
    expect(current_page).to_have_url(re.compile(r"/login"))


@then("werde ich zur Login-Seite umgeleitet")
def _then_redirected_to_login(current_page):
    expect(current_page).to_have_url(re.compile(r"/login"))
