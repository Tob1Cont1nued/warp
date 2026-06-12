import time
from playwright.sync_api import Page, Locator


class QuestionnairePage:
    """Page Object für /project/<id>."""

    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url
        # Sidebar
        self.brand_name: Locator = page.locator(".sidebar-brand-name")
        self.brand_tagline: Locator = page.locator(".sidebar-brand-tagline")
        self.projects_sidebar: Locator = page.locator(".sidebar-projects")
        self.new_project_btn: Locator = page.locator(".sidebar-new-btn")
        self.logout_link: Locator = page.locator(".sidebar-logout")
        self.download_buttons: Locator = page.locator(".sidebar-download-btn")
        # Hauptinhalt
        self.answer_selects: Locator = page.locator(".js-answer")
        self.note_textareas: Locator = page.locator(".js-note")
        self.progress_bar: Locator = page.locator(".progress-bar")
        self.auswertung_section: Locator = page.locator("#auswertung-section")

    def goto(self, project_id: int) -> "QuestionnairePage":
        self.page.goto(f"{self.base_url}/project/{project_id}")
        return self

    def select_first_answer(self) -> str:
        """Wählt die erste nicht-leere Antwort-Option; gibt den Wert zurück."""
        select = self.answer_selects.first
        options = select.locator("option").all()
        non_empty = [o for o in options if o.get_attribute("value")]
        assert non_empty, "Keine wählbaren Antwort-Optionen vorhanden"
        value = non_empty[0].get_attribute("value")
        select.select_option(value)
        return value

    def wait_for_autosave(self) -> None:
        time.sleep(1.0)

    def create_first_project(self, name: str) -> None:
        """Legt erstes Projekt an, wenn auf /project/new weitergeleitet wurde."""
        self.page.fill("#name", name)
        self.page.click("button[type=submit]")
        self.page.wait_for_load_state("networkidle")
