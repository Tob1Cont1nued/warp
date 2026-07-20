"""Page Object für /project/<id> – Auswertungs-Tab und Handlungsempfehlungen."""
import time
from playwright.sync_api import Page, Locator


class ProjectPage:
    """Page Object für /project/<id>."""

    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url

        # Tabs
        self.tab_fragenkatalog: Locator = page.locator('button[data-tab="fragenkatalog"]')
        self.tab_auswertung:    Locator = page.locator('button[data-tab="auswertung"]')
        self.tab_ki:            Locator = page.locator('button[data-tab="ki"]')

        # Fortschritt
        self.progress_text: Locator = page.locator("#js-answered")

        # Handlungsempfehlungen
        self.recs_card:       Locator = page.locator("#js-recs-card")
        self.recs_list:       Locator = page.locator("#js-recs-list")
        self.recs_toggle_btn: Locator = page.locator("#js-recs-toggle")
        self.cat_headers:     Locator = page.locator(".rec-cat-header")
        self.cat_bodies:      Locator = page.locator(".rec-cat-body")

    def goto(self, project_id: int) -> "ProjectPage":
        self.page.goto(f"{self.base_url}/project/{project_id}")
        self.page.wait_for_load_state("networkidle")
        return self

    def open_auswertung_tab(self) -> None:
        self.tab_auswertung.click()
        # JS braucht einen Moment um buildRecs() auszuführen
        self.page.wait_for_timeout(400)

    def answer_question(self, qid: str, value: str) -> None:
        """Setzt eine Antwort per data-qid-Selektor. value: voll|teil|kaum|nicht"""
        sel = self.page.locator(f'select[data-qid="{qid}"]')
        sel.select_option(value)
        time.sleep(0.3)  # Autosave-Debounce

    def category_count(self) -> int:
        """Anzahl der sichtbaren Kategorie-Abschnitte in den Empfehlungen."""
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

    def create_project(self, name: str = "Pytest Recs Test") -> int:
        """Legt ein neues Projekt an und gibt die Projekt-ID zurück."""
        import re
        self.page.goto(f"{self.base_url}/project/new")
        self.page.wait_for_load_state("networkidle")
        self.page.fill("#name", name)
        self.page.click('button[type="submit"]')
        self.page.wait_for_url(re.compile(r"/project/\d+$"), timeout=30_000)
        self.page.wait_for_load_state("networkidle")
        url = self.page.url
        return int(url.rstrip("/").rsplit("/", 1)[-1])
