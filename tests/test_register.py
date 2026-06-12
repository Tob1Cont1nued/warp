"""
Registrierungs-Seite (/register) – Oberflächentests (Page Object Model)
========================================================================
Positiv:
  P1  Alle UI-Elemente der Registrierungs-Seite sind sichtbar
  P2  Neuer Benutzer wird angelegt und landet auf Projekt-Seite
  P3  Link „Bereits registriert?" navigiert zur Login-Seite

Negativ:
  N1  Bereits vergebener Benutzername → Fehlermeldung
  N2  Passwörter stimmen nicht überein → Fehlermeldung
  N3  Passwort kürzer als 6 Zeichen → Fehlermeldung
"""

import time
from playwright.sync_api import expect
from conftest import TEST_USER


def _unique_user() -> str:
    return f"_pytest_reg_{int(time.time() * 1000) % 100_000}"


# ── Positiv-Tests ────────────────────────────────────────────────────────────

def test_p1_register_seite_elemente_sichtbar(register_page):
    register_page.goto()
    expect(register_page.brand_name).to_have_text("WARP")
    expect(register_page.username).to_be_visible()
    expect(register_page.display_name).to_be_visible()
    expect(register_page.password).to_be_visible()
    expect(register_page.password2).to_be_visible()
    expect(register_page.submit_btn).to_be_visible()
    expect(register_page.switch_link).to_be_visible()


def test_p2_neuer_benutzer_wird_angelegt_und_weitergeleitet(register_page):
    register_page.register(_unique_user(), "sicher123", display_name="Playwright User")
    assert "/project" in register_page.page.url


def test_p3_anmelden_link_navigiert_zur_login_seite(register_page, base_url):
    register_page.goto()
    register_page.switch_link.click()
    expect(register_page.page).to_have_url(f"{base_url}/login")


# ── Negativ-Tests ────────────────────────────────────────────────────────────

def test_n1_doppelter_benutzername_zeigt_fehler(register_page):
    register_page.register(TEST_USER["username"], "irgendetwas123")
    expect(register_page.error).to_be_visible()
    expect(register_page.error).to_contain_text("vergeben")


def test_n2_passwort_mismatch_zeigt_fehler(register_page):
    register_page.register(_unique_user(), "passwort1", password2="passwort2")
    expect(register_page.error).to_be_visible()
    expect(register_page.error).to_contain_text("überein")


def test_n3_passwort_zu_kurz_zeigt_fehler(register_page):
    register_page.register(_unique_user(), "abc")
    expect(register_page.error).to_be_visible()
    expect(register_page.error).to_contain_text("6 Zeichen")
