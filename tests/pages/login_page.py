from playwright.sync_api import Page, Locator


class LoginPage:
    """Page Object für /login."""

    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url
        self.brand_name: Locator = page.locator(".login-brand-name")
        self.brand_tagline: Locator = page.locator(".login-brand-tagline")
        self.username: Locator = page.locator("#username")
        self.password: Locator = page.locator("#password")
        self.submit_btn: Locator = page.locator("button[type=submit]")
        self.switch_link: Locator = page.locator("a.login-switch-link")
        self.error: Locator = page.locator(".login-error")

    def goto(self) -> "LoginPage":
        self.page.goto(f"{self.base_url}/login")
        return self

    def login(self, username: str, password: str) -> None:
        self.goto()
        self.username.fill(username)
        self.password.fill(password)
        self.submit_btn.click()
        self.page.wait_for_load_state("networkidle")
