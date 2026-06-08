"""Dashboard page object for the Secure S3 File Portal."""

from __future__ import annotations

from selenium.webdriver.common.by import By

from tests.pages.base_page import BasePage

Locator = tuple[str, str]


class DashboardPage(BasePage):
    """Represent the main portal dashboard page."""

    URL_PATH = "/"

    PAGE_HERO: Locator = (By.CSS_SELECTOR, "[data-testid='portal-hero']")
    PAGE_HEADING: Locator = (By.CSS_SELECTOR, "[data-testid='page-heading']")
    STORAGE_STATUS_PANEL: Locator = (
        By.CSS_SELECTOR,
        "[data-testid='storage-status-panel']",
    )

    def is_loaded(self) -> bool:
        """Return whether the main dashboard elements are present and visible."""
        page_hero = self.driver.find_elements(*self.PAGE_HERO)
        headings = self.driver.find_elements(*self.PAGE_HEADING)
        storage_panels = self.driver.find_elements(*self.STORAGE_STATUS_PANEL)

        if not page_hero or not headings or not storage_panels:
            return False

        return (
            page_hero[0].is_displayed()
            and headings[0].is_displayed()
            and storage_panels[0].is_displayed()
        )
