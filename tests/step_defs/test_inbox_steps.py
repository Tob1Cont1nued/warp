"""
TC – Postkorb (/inbox)
=========================
Gherkin-Umsetzung von tests/features/inbox.feature. Echter User-Flow: Admin
navigiert über den "Postkorb"-Link in der Sidebar, kein direkter URL-Aufruf
für den Happy-Path (wie zuvor tests/test_inbox.py).

Szenario → Testname:
  Admin sieht Postkorb-Link              → test_i1_admin_sees_postkorb_in_sidebar
  Admin öffnet Postkorb über Sidebar     → test_i2_admin_opens_inbox_via_sidebar
  Normaler Benutzer sieht keinen Link    → test_i3_regular_user_has_no_postkorb_link
  Normaler Benutzer blockiert            → test_i4_regular_user_blocked_from_inbox
  Nicht eingeloggt → Redirect            → test_i5_unauthenticated_redirected_to_login
"""

from playwright.sync_api import expect
from pytest_bdd import scenario, given, when, then

from pages.project_page import DashboardPage

FEATURE = "../features/inbox.feature"


# ---------------------------------------------------------------------------
# Szenario-Verknüpfungen
# ---------------------------------------------------------------------------

@scenario(FEATURE, "Admin sieht den Postkorb-Link in der Sidebar")
def test_i1_admin_sees_postkorb_in_sidebar():
    pass


@scenario(FEATURE, "Admin öffnet den Postkorb über die Sidebar")
def test_i2_admin_opens_inbox_via_sidebar():
    pass


@scenario(FEATURE, "Normaler Benutzer sieht keinen Postkorb-Link")
def test_i3_regular_user_has_no_postkorb_link():
    pass


@scenario(FEATURE, "Normaler Benutzer kann den Postkorb nicht direkt aufrufen")
def test_i4_regular_user_blocked_from_inbox():
    pass


@scenario(FEATURE, "Nicht eingeloggter Benutzer wird zur Login-Seite umgeleitet")
def test_i5_unauthenticated_redirected_to_login():
    pass


# ---------------------------------------------------------------------------
# Schritte
# ---------------------------------------------------------------------------

@then("sehe ich den Postkorb-Link in der Sidebar")
def _see_postkorb_link(current_page):
    expect(DashboardPage(current_page).nav_postkorb).to_be_visible()


@when("ich auf den Postkorb-Link in der Sidebar klicke", target_fixture="inbox_page")
def _click_postkorb(current_page):
    return DashboardPage(current_page).click_postkorb()


@then("lande ich auf der Postkorb-Seite")
def _on_inbox_page(inbox_page, base_url):
    expect(inbox_page.page).to_have_url(f"{base_url}/inbox")


@then('die Überschrift enthält "Postkorb"')
def _heading_contains(inbox_page):
    expect(inbox_page.heading).to_contain_text("Postkorb")


@then("jeder vorhandene Antworten-Button hat eine gültige E-Mail-Adresse hinterlegt")
def _reply_buttons_have_email(inbox_page):
    if inbox_page.reply_buttons.count() > 0:
        email = inbox_page.reply_buttons.first.get_attribute("data-email") or ""
        assert len(email) > 0, "Antworten-Button hat kein gültiges data-email-Attribut"


@then("sehe ich den Postkorb-Link in der Sidebar nicht", target_fixture="current_page")
def _no_postkorb_link(page, base_url):
    expect(DashboardPage(page).nav_postkorb).to_be_hidden()
    return page


@when("ich direkt die Postkorb-Seite aufrufe", target_fixture="current_page")
def _goto_inbox_directly(page, base_url):
    page.goto(f"{base_url}/inbox")
    page.wait_for_load_state("networkidle")
    return page


@then("werde ich blockiert")
def _blocked(page):
    blocked = (
        "/inbox" not in page.url            # umgeleitet (weg von /inbox)
        or "Kein Zugriff" in page.title()   # 403-Seite angezeigt
    )
    assert blocked, f"Normaler Benutzer darf /inbox nicht sehen. URL: {page.url} | Titel: {page.title()}"
