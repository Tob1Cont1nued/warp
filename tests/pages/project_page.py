"""Page Object für den Projekt-Workflow:
Dashboard → Neues Projekt anlegen → Fragen beantworten → Auswertung.
"""
import re
import time
from playwright.sync_api import Page, Locator, expect


class DashboardPage:
    """Page Object für /dashboard."""

    def __init__(self, page: Page) -> None:
        self.page = page
        # Sidebar-Elemente
        self.new_project_btn: Locator = page.locator("a.sidebar-new-btn")
        self.sidebar_projects:  Locator = page.locator(".sidebar-project-name")
        self.nav_postkorb:      Locator = page.locator("a.sidebar-nav-item", has_text="Postkorb")
        self.nav_dashboard:     Locator = page.locator("a.sidebar-nav-item", has_text="Dashboard")
        # Dashboard-Inhalt
        self.heading:           Locator = page.locator("h1", has_text="Dashboard")
        self.new_project_dashboard_btn: Locator = page.locator("a", has_text="+ Neues Projekt")

    def click_new_project(self) -> "NewProjectPage":
        """Klickt den '+'-Button in der Sidebar."""
        self.new_project_btn.click()
        self.page.wait_for_load_state("networkidle")
        return NewProjectPage(self.page)

    def click_project_in_sidebar(self, name: str) -> "ProjectPage":
        """Klickt ein Projekt anhand seines Namens in der Sidebar."""
        self.page.locator(".sidebar-project-name", has_text=name).first.click()
        self.page.wait_for_load_state("networkidle")
        return ProjectPage(self.page)

    def click_postkorb(self) -> "InboxPage":
        """Klickt den 'Postkorb'-Link in der Sidebar (nur für Admins sichtbar)."""
        self.nav_postkorb.click()
        self.page.wait_for_load_state("networkidle")
        return InboxPage(self.page)


class NewProjectPage:
    """Page Object für /project/new."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.name_input:  Locator = page.locator("#name")
        self.submit_btn:  Locator = page.locator('button[type="submit"]')

    def create(self, name: str) -> "ProjectPage":
        """Trägt den Projektnamen ein und klickt 'Erstellen'."""
        self.name_input.fill(name)
        self.submit_btn.click()
        self.page.wait_for_url(re.compile(r"/project/\d+$"), timeout=30_000)
        self.page.wait_for_load_state("networkidle")
        return ProjectPage(self.page)


class ProjectPage:
    """Page Object für /project/<id> — Fragenkatalog und Auswertung."""

    def __init__(self, page: Page) -> None:
        self.page = page
        # Tabs
        self.tab_fragenkatalog: Locator = page.locator('button[data-tab="fragenkatalog"]')
        self.tab_auswertung:    Locator = page.locator('button[data-tab="auswertung"]')
        # Handlungsempfehlungen
        self.recs_card:         Locator = page.locator("#js-recs-card")
        self.recs_list:         Locator = page.locator("#js-recs-list")
        self.recs_toggle_btn:   Locator = page.locator("#js-recs-toggle")
        self.cat_headers:       Locator = page.locator(".rec-cat-header")
        self.cat_bodies:        Locator = page.locator(".rec-cat-body")

    def answer_question(self, qid: str, value: str) -> None:
        """Wählt eine Antwort im Dropdown der Frage aus. value: voll|teil|kaum|nicht"""
        self.page.locator(f'select[data-qid="{qid}"]').select_option(value)
        time.sleep(0.3)  # Autosave-Debounce abwarten

    def click_auswertung_tab(self) -> None:
        """Klickt den 'Auswertung'-Reiter wie ein echter User."""
        self.tab_auswertung.click()
        self.page.wait_for_timeout(500)  # JS buildRecs() abwarten

    def category_count(self) -> int:
        return self.cat_headers.count()

    def toggle_category(self, index: int = 0) -> None:
        self.cat_headers.nth(index).click()
        self.page.wait_for_timeout(250)

    def toggle_recs_card(self) -> None:
        self.recs_toggle_btn.click()
        self.page.wait_for_timeout(250)

    def is_cat_body_visible(self, index: int = 0) -> bool:
        return self.cat_bodies.nth(index).is_visible()

    def is_recs_list_visible(self) -> bool:
        return self.recs_list.is_visible()


class InboxPage:
    """Page Object für /inbox (Postkorb)."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.heading:         Locator = page.locator("h1, h2").first
        self.reply_buttons:   Locator = page.locator('button.iab-btn', has_text="Antworten")
