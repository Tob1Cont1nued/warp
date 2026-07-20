"""
Postkorb (/inbox) – Frontend-Tests (echter User-Flow)
======================================================
Simuliert echtes User-Verhalten:
  Admin:   Login → Dashboard → 'Postkorb'-Link in Sidebar klicken
  User:    Login → Dashboard → 'Postkorb' ist NICHT in Sidebar sichtbar
  Kein Login: Direkt-URL /inbox → Redirect zur Login-Seite

  I1  Admin sieht 'Postkorb'-Link in der Sidebar
  I2  Admin öffnet Postkorb per Sidebar → Überschrift + Antworten-Button korrekt
  I3  Normaler Benutzer sieht KEINEN 'Postkorb'-Link in der Sidebar
  I4  Normaler Benutzer kann /inbox nicht per Direktzugriff öffnen (blockiert)
  I5  Nicht eingeloggter Benutzer wird beim Direktzugriff zu /login umgeleitet
"""

import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.project_page import DashboardPage, InboxPage
from conftest import ADMIN, TEST_USER


# ── I1: Admin sieht Postkorb-Link in der Sidebar ─────────────────────────────

def test_i1_admin_sees_postkorb_in_sidebar(page: Page, base_url: str):
    LoginPage(page, base_url).login(ADMIN["username"], ADMIN["password"])
    dashboard = DashboardPage(page)
    expect(dashboard.nav_postkorb).to_be_visible()


# ── I2: Admin öffnet Postkorb per Sidebar-Klick ───────────────────────────────

def test_i2_admin_opens_inbox_via_sidebar(page: Page, base_url: str):
    LoginPage(page, base_url).login(ADMIN["username"], ADMIN["password"])
    dashboard = DashboardPage(page)

    # User klickt 'Postkorb' in der Sidebar-Navigation
    inbox = dashboard.click_postkorb()

    # URL ist /inbox und Überschrift ist sichtbar
    expect(page).to_have_url(f"{base_url}/inbox")
    expect(inbox.heading).to_contain_text("Postkorb")

    # Falls Nachrichten vorhanden: Antworten-Button hat data-email-Attribut
    if inbox.reply_buttons.count() > 0:
        email = inbox.reply_buttons.first.get_attribute("data-email") or ""
        assert len(email) > 0, "Antworten-Button hat kein gültiges data-email-Attribut"


# ── I3: Normaler Benutzer sieht keinen Postkorb-Link ─────────────────────────

def test_i3_regular_user_has_no_postkorb_link(page: Page, base_url: str):
    LoginPage(page, base_url).login(TEST_USER["username"], TEST_USER["password"])
    dashboard = DashboardPage(page)

    # 'Postkorb'-Link darf in der Sidebar nicht sichtbar sein
    expect(dashboard.nav_postkorb).to_be_hidden()


# ── I4: Normaler Benutzer kann /inbox nicht per URL öffnen ───────────────────

def test_i4_regular_user_blocked_from_inbox(page: Page, base_url: str):
    LoginPage(page, base_url).login(TEST_USER["username"], TEST_USER["password"])

    # User tippt /inbox direkt in die Adresszeile
    page.goto(f"{base_url}/inbox")
    page.wait_for_load_state("networkidle")

    blocked = (
        "/inbox" not in page.url            # umgeleitet (weg von /inbox)
        or "Kein Zugriff" in page.title()   # 403-Seite angezeigt
    )
    assert blocked, (
        f"Normaler Benutzer darf /inbox nicht sehen. "
        f"URL: {page.url} | Titel: {page.title()}"
    )


# ── I5: Nicht eingeloggt → Redirect zu /login ────────────────────────────────

def test_i5_unauthenticated_redirected_to_login(page: Page, base_url: str):
    # Kein Login – User tippt /inbox direkt in die Adresszeile
    page.goto(f"{base_url}/inbox")
    page.wait_for_load_state("networkidle")

    assert "/login" in page.url, (
        f"Nicht eingeloggter User sollte zu /login umgeleitet werden. "
        f"Tatsächliche URL: {page.url}"
    )


