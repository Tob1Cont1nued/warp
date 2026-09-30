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
        # Abmelden sitzt seit dem Profil-Dropdown-Umbau oben rechts in der
        # Topbar statt in der Sidebar - Button + (versteckter) Menüpunkt.
        self.profile_btn: Locator = page.locator("#js-profile-btn")
        self.logout_link: Locator = page.locator(".profile-dropdown-item.danger")
        # Hauptinhalt
        self.answer_selects: Locator = page.locator(".js-answer")
        self.note_textareas: Locator = page.locator(".js-note")
        self.progress_bar: Locator = page.locator(".progress-bar")
        # Die Seite ist jetzt tab-basiert (Fragen/Auswertung/Dokumente/Verwalten);
        # der Auswertung-Inhalt (#tab-auswertung) ist erst nach Klick auf den
        # Tab-Button sichtbar, der Button selbst aber immer.
        self.auswertung_tab_btn: Locator = page.locator('button[data-tab="auswertung"]')

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
