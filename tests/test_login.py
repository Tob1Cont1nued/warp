"""
Login-Seite (/login) – Oberflächentests (Page Object Model)
===========================================================
Positiv:
  P1  Alle UI-Elemente der Login-Seite sind sichtbar
  P2  Admin-Login leitet auf /admin weiter
  P3  User-Login leitet auf /project/... weiter

Negativ:
  N1  Falsches Passwort → Fehlermeldung
  N2  Nicht existenter Benutzer → Fehlermeldung
  N3  Gesperrter Benutzer → spezifische Meldung ("gesperrt")
"""

from playwright.sync_api import expect
from conftest import ADMIN, TEST_USER
from pages.admin_page import AdminPage

LOCKED_USER = "_pytest_will_be_locked"
LOCKED_PW   = "locked_pw_123"


# ── Positiv-Tests ────────────────────────────────────────────────────────────

def test_p1_login_seite_elemente_sichtbar(login_page):
    login_page.goto()
    expect(login_page.brand_name).to_have_text("WARP")
    expect(login_page.brand_tagline).to_be_visible()
    expect(login_page.username).to_be_visible()
    expect(login_page.password).to_be_visible()
    expect(login_page.submit_btn).to_be_visible()
    expect(login_page.switch_link).to_be_visible()


def test_p2_admin_login_leitet_auf_admin_weiter(login_page, base_url):
    login_page.login(ADMIN["username"], ADMIN["password"])
    expect(login_page.page).to_have_url(f"{base_url}/admin")


def test_p3_user_login_leitet_auf_projekt_weiter(login_page):
    login_page.login(TEST_USER["username"], TEST_USER["password"])
    assert "/project" in login_page.page.url


# ── Negativ-Tests ────────────────────────────────────────────────────────────

def test_n1_falsches_passwort_zeigt_fehler(login_page):
    login_page.goto()
    login_page.username.fill(ADMIN["username"])
    login_page.password.fill("voellig_falsch")
    login_page.submit_btn.click()
    expect(login_page.error).to_be_visible()


def test_n2_unbekannter_benutzer_zeigt_fehler(login_page):
    login_page.goto()
    login_page.username.fill("existiert_nicht_xyz")
    login_page.password.fill("egal")
    login_page.submit_btn.click()
    expect(login_page.error).to_be_visible()


def test_n3_gesperrter_benutzer_zeigt_spezifische_meldung(login_page, base_url):
    """Legt einen Benutzer via Admin-UI an, sperrt ihn, prüft Login-Fehlermeldung."""
    # Als Admin einloggen, Konto anlegen und sperren
    login_page.login(ADMIN["username"], ADMIN["password"])
    admin = AdminPage(login_page.page, base_url)
    admin.create_user(LOCKED_USER, LOCKED_PW)
    admin.lock_user(LOCKED_USER)

    # Ausloggen → landet auf /login
    login_page.page.goto(f"{base_url}/logout")
    login_page.page.wait_for_load_state("networkidle")

    # Mit gesperrtem Konto anmelden
    login_page.username.fill(LOCKED_USER)
    login_page.password.fill(LOCKED_PW)
    login_page.submit_btn.click()
    expect(login_page.error).to_contain_text("gesperrt")
    expect(login_page.page).to_have_url(f"{base_url}/login")
