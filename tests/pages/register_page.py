from typing import Optional
from playwright.sync_api import Page, Locator


class RegisterPage:
    """Page Object für /register."""

    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url
        self.brand_name: Locator = page.locator(".login-brand-name")
        self.username: Locator = page.locator("#username")
        self.display_name: Locator = page.locator("#display_name")
        self.password: Locator = page.locator("#password")
        self.password2: Locator = page.locator("#password2")
        self.submit_btn: Locator = page.locator("button[type=submit]")
        self.switch_link: Locator = page.locator("a.login-switch-link")
        self.error: Locator = page.locator(".login-error")

    def goto(self) -> "RegisterPage":
        self.page.goto(f"{self.base_url}/register")
        return self

    def register(
        self,
        username: str,
        password: str,
        display_name: str = "",
        password2: Optional[str] = None,
    ) -> None:
        self.goto()
        self.username.fill(username)
        if display_name:
            self.display_name.fill(display_name)
        self.password.fill(password)
        self.password2.fill(password2 if password2 is not None else password)
        self.submit_btn.click()
        self.page.wait_for_load_state("networkidle")
