"""
TC – Profil & Benachrichtigungen (_profile_button.html)
===========================================================
Gherkin-Umsetzung von tests/features/profile.feature.

Szenario → Testname:
  Profil-Button auf mehreren Seiten sichtbar  → test_p1_profilbutton_auf_mehreren_seiten_sichtbar
  Administration für Superuser sichtbar       → test_p2_administration_sichtbar_fuer_superuser
  Glocke sichtbar für Admin                   → test_p3_glocke_sichtbar_fuer_admin
  Glocke zeigt Badge bei neuer Nachricht      → test_p4_glocke_zeigt_badge_bei_neuer_nachricht
  Administration nicht für einfachen Admin    → test_n1_administration_nicht_fuer_einfachen_admin
  Glocke nicht sichtbar für normalen Benutzer → test_n2_glocke_nicht_sichtbar_fuer_normalen_benutzer
"""

import os
import time

import requests
from playwright.sync_api import expect
from pytest_bdd import scenario, given, when, then, parsers

from pages.login_page import LoginPage

FEATURE = "../features/profile.feature"
API_KEY = os.environ.get("WARP_INBOX_API_KEY", "test-api-key-123")


def _unique_user() -> str:
    return f"_profile_test_{int(time.time() * 1000) % 100_000}"


# ---------------------------------------------------------------------------
# Szenario-Verknüpfungen
# ---------------------------------------------------------------------------

@scenario(FEATURE, "Profil-Button ist auf mehreren Seiten sichtbar")
def test_p1_profilbutton_auf_mehreren_seiten_sichtbar():
    pass


@scenario(FEATURE, "Dropdown zeigt Administration für Superuser")
def test_p2_administration_sichtbar_fuer_superuser():
    pass


@scenario(FEATURE, "Postkorb-Glocke ist für Admins sichtbar")
def test_p3_glocke_sichtbar_fuer_admin():
    pass


@scenario(FEATURE, "Glocke zeigt einen Badge bei neuer Nachricht")
def test_p4_glocke_zeigt_badge_bei_neuer_nachricht():
    pass


@scenario(FEATURE, "Administration ist für einfache Admins nicht sichtbar")
def test_n1_administration_nicht_fuer_einfachen_admin():
    pass


@scenario(FEATURE, "Glocke ist für normale Benutzer nicht sichtbar")
def test_n2_glocke_nicht_sichtbar_fuer_normalen_benutzer():
    pass


# ---------------------------------------------------------------------------
# Schritte
# ---------------------------------------------------------------------------

@then("sehe ich den Profil-Button auf dem Dashboard")
def _profile_btn_dashboard(current_page, base_url):
    current_page.goto(f"{base_url}/dashboard")
    expect(current_page.locator("#js-profile-btn")).to_be_visible()


@then("sehe ich den Profil-Button auf der Vorlagen-Seite")
def _profile_btn_vorlagen(current_page, base_url):
    current_page.goto(f"{base_url}/vorlagen")
    expect(current_page.locator("#js-profile-btn")).to_be_visible()


@when("ich den Profil-Button öffne")
def _open_profile_dropdown(current_page):
    current_page.click("#js-profile-btn")


@then(parsers.parse('sehe ich den Menüpunkt "{text}"'))
def _see_menu_item(current_page, text):
    expect(current_page.locator(".profile-dropdown-item", has_text=text)).to_be_visible()


@then(parsers.parse('sehe ich den Menüpunkt "{text}" nicht'))
def _no_menu_item(current_page, text):
    expect(current_page.locator(".profile-dropdown-item", has_text=text)).to_have_count(0)


@then("sehe ich die Postkorb-Glocke")
def _see_bell(current_page):
    expect(current_page.locator("#js-bell-link")).to_be_visible()


@then("sehe ich die Postkorb-Glocke nicht")
def _no_bell(current_page):
    expect(current_page.locator("#js-bell-link")).to_have_count(0)


@when("im Postkorb eine neue Nachricht eintrifft")
def _new_inbox_message(base_url):
    suffix = str(int(time.time() * 1000))
    requests.post(
        f"{base_url}/api/inbox",
        json={
            "userName": f"Profiltest {suffix}",
            "userEmail": f"profiltest{suffix}@example.com",
            "recommendation": "Testnachricht für das Glocken-Badge (Playwright).",
        },
        headers={"X-API-Key": API_KEY},
        timeout=10,
    )


@when("ich die Seite neu lade")
def _reload(current_page):
    current_page.reload()
    current_page.wait_for_load_state("networkidle")


@then("zeigt die Glocke ein Badge größer als 0")
def _bell_badge_positive(current_page):
    badge = current_page.locator("#js-bell-badge")
    expect(badge).to_be_visible()
    count_text = badge.inner_text().strip()
    assert count_text.isdigit() and int(count_text) > 0, f"Unerwarteter Badge-Text: {count_text!r}"


@given('ich habe einen Benutzer mit der Rolle "admin" angelegt', target_fixture="new_user_creds")
def _create_plain_admin(admin_page):
    username = _unique_user()
    password = "plain_admin_pw1"
    admin_page.create_user(username, password, role="admin")
    return {"username": username, "password": password}


@when("ich mich abmelde und mit diesem Konto neu anmelde", target_fixture="current_page")
def _logout_and_login_as(current_page, base_url, new_user_creds):
    current_page.goto(f"{base_url}/logout")
    current_page.wait_for_load_state("networkidle")
    LoginPage(current_page, base_url).login(new_user_creds["username"], new_user_creds["password"])
    current_page.goto(f"{base_url}/dashboard")
    return current_page
