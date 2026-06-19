from playwright.sync_api import Page

from config.sandbox import APP_BASE_URL


class BasePage:
    """Shared Playwright page wrapper for navigation and common utilities."""

    def __init__(self, page: Page, base_url: str = APP_BASE_URL) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/")

    def goto(self, path: str = "") -> None:
        if not path:
            url = self.base_url
        elif path.startswith("/"):
            url = f"{self.base_url}{path}"
        else:
            url = f"{self.base_url}/{path}"
        self.page.goto(url)

    def wait_for_load(self) -> None:
        self.page.wait_for_load_state("networkidle")
