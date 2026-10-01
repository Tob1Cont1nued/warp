"""
Profil & Benachrichtigungen – Frontend-Tests (_profile_button.html)
======================================================================
Positiv:
  P1  Profil-Button oben rechts ist auf mehreren Seiten sichtbar, nicht nur im Dashboard
  P2  Dropdown zeigt "Administration" für Superuser
  P3  Postkorb-Glocke ist für Admins sichtbar
  P4  Glocke zeigt einen Badge, sobald eine neue Postkorb-Nachricht eintrifft

Negativ:
  N1  Dropdown zeigt "Administration" NICHT für einen einfachen Admin (kein Superuser)
  N2  Glocke ist für normale Benutzer (kein Admin) NICHT sichtbar
"""

import os
import time

import requests
from playwright.sync_api import Page, expect

from conftest import ADMIN, TEST_USER
from pages.login_page import LoginPage
from pages.admin_page import AdminPage

API_KEY = os.environ.get("WARP_INBOX_API_KEY", "test-api-key-123")


def _unique_user() -> str:
    return f"_profile_test_{int(time.time() * 1000) % 100_000}"


def _post_inbox_message(base_url: str, suffix: str) -> None:
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


# ── Positiv-Tests ────────────────────────────────────────────────────────────

def test_p1_profilbutton_auf_mehreren_seiten_sichtbar(page: Page, base_url: str):
    """Der Profil-Button saß früher nur im Dashboard; jetzt in der Topbar jeder Seite."""
    LoginPage(page, base_url).login(TEST_USER["username"], TEST_USER["password"])
    for path in ("/dashboard", "/vorlagen"):
        page.goto(f"{base_url}{path}")
        expect(page.locator("#js-profile-btn")).to_be_visible()


def test_p2_administration_sichtbar_fuer_superuser(page: Page, base_url: str):
    LoginPage(page, base_url).login(ADMIN["username"], ADMIN["password"])  # admin/warp2024 = superuser
    page.goto(f"{base_url}/dashboard")
    page.click("#js-profile-btn")
    expect(page.locator(".profile-dropdown-item", has_text="Administration")).to_be_visible()


def test_p3_glocke_sichtbar_fuer_admin(page: Page, base_url: str):
    LoginPage(page, base_url).login(ADMIN["username"], ADMIN["password"])
    page.goto(f"{base_url}/dashboard")
    expect(page.locator("#js-bell-link")).to_be_visible()


def test_p4_glocke_zeigt_badge_bei_neuer_nachricht(page: Page, base_url: str):
    LoginPage(page, base_url).login(ADMIN["username"], ADMIN["password"])
    _post_inbox_message(base_url, suffix=str(int(time.time() * 1000)))
    page.goto(f"{base_url}/dashboard")
    page.wait_for_load_state("networkidle")  # Poller ruft /api/inbox/count sofort beim Laden auf
    badge = page.locator("#js-bell-badge")
    expect(badge).to_be_visible()
    count_text = badge.inner_text().strip()
    assert count_text.isdigit() and int(count_text) > 0, f"Unerwarteter Badge-Text: {count_text!r}"


# ── Negativ-Tests ────────────────────────────────────────────────────────────

def test_n1_administration_nicht_fuer_einfachen_admin(page: Page, base_url: str):
    """Nur Superuser dürfen die Benutzerverwaltung sehen - ein normaler Admin (Postkorb-
    Zugriff, aber kein Superuser) darf "Administration" im Dropdown nicht sehen."""
    LoginPage(page, base_url).login(ADMIN["username"], ADMIN["password"])
    admin = AdminPage(page, base_url).goto()
    plain_admin = _unique_user()
    admin.create_user(plain_admin, "plain_admin_pw1", role="admin")

    page.goto(f"{base_url}/logout")
    page.wait_for_load_state("networkidle")
    LoginPage(page, base_url).login(plain_admin, "plain_admin_pw1")
    page.goto(f"{base_url}/dashboard")
    page.click("#js-profile-btn")
    expect(page.locator(".profile-dropdown-item", has_text="Administration")).to_have_count(0)


def test_n2_glocke_nicht_sichtbar_fuer_normalen_benutzer(page: Page, base_url: str):
    LoginPage(page, base_url).login(TEST_USER["username"], TEST_USER["password"])
    page.goto(f"{base_url}/dashboard")
    expect(page.locator("#js-bell-link")).to_have_count(0)
