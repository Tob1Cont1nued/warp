"""
Admin-Seite (/admin) – Oberflächentests (Page Object Model)
============================================================
Positiv:
  P1  Alle UI-Elemente auf der Admin-Seite sind sichtbar
  P2  Admin kann neuen Benutzer anlegen – erscheint anschließend in der Liste
  P3  Admin kann Benutzer sperren – Badge "gesperrt" wird angezeigt
  P4  Admin kann ein eigenes Projekt anlegen (POST /project/new → /project/<id>)

Negativ:
  N1  Normaler Benutzer kann /admin nicht aufrufen (403)
  N2  Nicht eingeloggter Benutzer wird zur Login-Seite umgeleitet
"""

import re
import time
from playwright.sync_api import Page, expect
from conftest import TEST_USER
from pages.login_page import LoginPage
from pages.admin_page import AdminPage


def _unique_user() -> str:
    return f"_admin_test_{int(time.time() * 1000) % 100_000}"


# ── Positiv-Tests ────────────────────────────────────────────────────────────

def test_p1_admin_seite_elemente_sichtbar(admin_page, base_url):
    expect(admin_page.page).to_have_url(f"{base_url}/admin")
    expect(admin_page.new_user_form).to_be_visible()
    expect(admin_page.username_input).to_be_visible()
    expect(admin_page.password_input).to_be_visible()
    expect(admin_page.submit_btn).to_be_visible()
    expect(admin_page.user_cards.first).to_be_visible()


def test_p2_admin_legt_benutzer_an(admin_page, base_url):
    new_user = _unique_user()
    admin_page.create_user(new_user, "testpasswort1")
    expect(admin_page.page).to_have_url(f"{base_url}/admin")
    expect(admin_page.get_user_card(new_user)).to_be_visible()


def test_p3_admin_sperrt_benutzer(admin_page):
    new_user = _unique_user()
    admin_page.create_user(new_user, "testpasswort1")
    admin_page.lock_user(new_user)
    assert admin_page.is_user_locked(new_user)


def test_p4_admin_kann_eigenes_projekt_anlegen(admin_page, base_url):
    """Admins durften früher kein eigenes Projekt anlegen (Bug, Fix 5c2e6fa) -
    seitdem landet POST /project/new auch für Admins auf /project/<id>."""
    admin_page.page.goto(f"{base_url}/project/new")
    admin_page.page.fill("#name", "AdminProjektTest")
    admin_page.page.click("button[type=submit]")
    expect(admin_page.page).to_have_url(re.compile(r"/project/\d+$"))
    # Der Projektname taucht mehrfach auf (Sidebar-Liste + Titel etc.) - hier
    # zählt nur, dass er überhaupt sichtbar ist, nicht die exakte Anzahl.
    expect(admin_page.page.locator("text=AdminProjektTest").first).to_be_visible()


# ── Negativ-Tests ────────────────────────────────────────────────────────────

def test_n1_normaler_benutzer_kann_admin_nicht_aufrufen(page: Page, base_url):
    LoginPage(page, base_url).login(TEST_USER["username"], TEST_USER["password"])
    response = page.goto(f"{base_url}/admin")
    assert response.status == 403


def test_n2_nicht_eingeloggter_benutzer_wird_umgeleitet(page: Page, base_url):
    page.goto(f"{base_url}/admin")
    expect(page).to_have_url(re.compile(r"/login"))
