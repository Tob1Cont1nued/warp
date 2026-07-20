"""
Postkorb (/inbox) – Frontend-Tests
====================================
Testet den Postkorb-Bereich (nur für Admins zugänglich):

  I1  Admin kann /inbox aufrufen (200)
  I2  Normaler Benutzer erhält 403
  I3  Nicht eingeloggter Benutzer wird zur Login-Seite umgeleitet
  I4  Postkorb-Seite zeigt den Seiten-Titel "Postkorb"
  I5  "Antworten"-Button hat ein mailto:-href-Attribut (wenn Nachrichten vorhanden)

Hinweis: Tests laufen gegen den lokalen Flask-Server (http://127.0.0.1:5000).
"""

import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from conftest import ADMIN, TEST_USER


# ── I1: Admin-Zugriff ─────────────────────────────────────────────────────────

def test_i1_admin_can_access_inbox(page: Page, base_url: str):
    LoginPage(page, base_url).login(ADMIN["username"], ADMIN["password"])
    page.goto(f"{base_url}/inbox")
    page.wait_for_load_state("networkidle")

    expect(page).to_have_url(f"{base_url}/inbox")
    assert page.title() != "WARP · Kein Zugriff", "Admin darf /inbox nicht mit 403 sehen"


# ── I2: Normaler Benutzer → kein Zugriff auf /inbox ──────────────────────────

def test_i2_regular_user_denied(page: Page, base_url: str):
    LoginPage(page, base_url).login(TEST_USER["username"], TEST_USER["password"])
    page.goto(f"{base_url}/inbox")
    page.wait_for_load_state("networkidle")

    # Normaler User bekommt entweder 403-Seite oder Redirect zur Login-/Dashboard-Seite
    blocked = (
        "/inbox" not in page.url           # umgeleitet (weg von /inbox)
        or "Kein Zugriff" in page.title()  # 403-Seite angezeigt
    )
    assert blocked, f"Normaler Benutzer darf /inbox nicht sehen. URL: {page.url}, Titel: {page.title()}"


# ── I3: Nicht eingeloggt → Redirect zur Login-Seite ──────────────────────────

def test_i3_unauthenticated_redirected_to_login(page: Page, base_url: str):
    response = page.goto(f"{base_url}/inbox")
    page.wait_for_load_state("networkidle")

    # Entweder 401/403 oder Redirect zur Login-Seite
    is_login_page = "/login" in page.url
    is_blocked     = response.status in (401, 403)
    assert is_login_page or is_blocked, (
        f"Unauthenticated user sollte zu /login umgeleitet werden oder 401/403 erhalten. "
        f"URL: {page.url}, Status: {response.status}"
    )


# ── I4+I5: Postkorb-Titel und Antworten-Button (ein Login) ───────────────────

def test_i4_inbox_ui(page: Page, base_url: str):
    """Admin sieht Postkorb-Heading; Antworten-Button hat data-email (wenn Meldungen da)."""
    page.set_default_timeout(60_000)
    LoginPage(page, base_url).login(ADMIN["username"], ADMIN["password"])
    page.goto(f"{base_url}/inbox")
    page.wait_for_load_state("networkidle")

    # I4: Überschrift "Postkorb" sichtbar
    heading = page.locator("h1, h2").first
    expect(heading).to_contain_text("Postkorb")

    # I5: Antworten-Button prüfen falls Nachrichten vorhanden
    reply_buttons = page.locator('button.iab-btn:has-text("Antworten")')
    if reply_buttons.count() == 0:
        return  # kein Skip nötig – Postkorb leer ist valider Zustand

    mailto_ok = page.evaluate("""
        () => {
            const btn = document.querySelector('button.iab-btn[onclick*="replyMail"]');
            return btn ? (btn.dataset.email || '').length > 0 : false;
        }
    """)
    assert mailto_ok, "Antworten-Button hat kein gültiges data-email-Attribut"
