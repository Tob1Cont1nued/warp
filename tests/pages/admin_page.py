from playwright.sync_api import Page, Locator


class AdminPage:
    """Page Object für /admin."""

    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url
        # Formular: Neuen Benutzer anlegen
        self.new_user_form: Locator = page.locator(".admin-new-user-form")
        self.username_input: Locator = page.locator(".admin-new-user-form #username")
        self.display_name_input: Locator = page.locator(".admin-new-user-form #display_name")
        self.password_input: Locator = page.locator(".admin-new-user-form #password")
        self.submit_btn: Locator = page.locator(".admin-new-user-form button[type=submit]")
        # Benutzerliste
        self.user_cards: Locator = page.locator(".admin-user-card")

    def goto(self) -> "AdminPage":
        self.page.goto(f"{self.base_url}/admin")
        return self

    def create_user(self, username: str, password: str, display_name: str = "") -> None:
        if display_name:
            self.display_name_input.fill(display_name)
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.submit_btn.click()
        self.page.wait_for_load_state("networkidle")

    def get_user_card(self, username: str) -> Locator:
        return self.user_cards.filter(has_text=username)

    def lock_user(self, username: str) -> None:
        self.get_user_card(username).locator("button:has-text('Sperren')").click()
        self.page.wait_for_load_state("networkidle")

    def is_user_locked(self, username: str) -> bool:
        return self.get_user_card(username).locator(".admin-locked-badge").is_visible()
