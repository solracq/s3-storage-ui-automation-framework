"""Access denied page object for the Secure S3 File Portal."""

from __future__ import annotations

from typing import TYPE_CHECKING

from selenium.webdriver.common.by import By

from tests.pages.base_page import BasePage

if TYPE_CHECKING:
    from tests.pages.dashboard.dashboard_page import DashboardPage
    from tests.pages.login.login_page import LoginPage

Locator = tuple[str, str]


class AccessDeniedPage(BasePage):
    """
    Represent the access denied page.
    """

    URL_PATH = "/access-denied"

    PAGE_ROOT: Locator = (By.CSS_SELECTOR, "[data-testid='access-denied-page']")
    PAGE_HEADING: Locator = (By.CSS_SELECTOR, "[data-testid='access-denied-heading']")
    PAGE_MESSAGE: Locator = (By.CSS_SELECTOR, "[data-testid='access-denied-message']")
    BACK_LINK: Locator = (By.CSS_SELECTOR, "[data-testid='back-to-dashboard-link']")

    # ### Helper Methods ###

    def is_loaded(self) -> bool:
        """
        Helper: return whether the access denied page elements are present and visible.
        """
        page_roots = self.driver.find_elements(*self.PAGE_ROOT)
        headings = self.driver.find_elements(*self.PAGE_HEADING)
        messages = self.driver.find_elements(*self.PAGE_MESSAGE)

        if not page_roots or not headings or not messages:
            return False

        return (
            page_roots[0].is_displayed()
            and headings[0].is_displayed()
            and messages[0].is_displayed()
        )

    def get_message_text(self) -> str:
        """
        Helper: return the access denied message shown on the page.
        """
        return self.driver.find_element(*self.PAGE_MESSAGE).text.strip()

    def get_back_link_text(self) -> str:
        """
        Helper: return the text shown in the back navigation link.
        """
        return self.driver.find_element(*self.BACK_LINK).text.strip()

    # ### Action Methods ###

    def click_back_link(self) -> "DashboardPage | LoginPage":
        """
        Click the back link and return the next page object based on the destination.
        """
        back_link = self.driver.find_element(*self.BACK_LINK)
        destination = back_link.get_attribute("href") or ""
        back_link.click()

        if destination.endswith("/login"):
            # Runtime import stays local to avoid circular imports between page objects.
            from tests.pages.login.login_page import LoginPage

            return LoginPage(self.driver)

        # Runtime import stays local to avoid circular imports between page objects.
        from tests.pages.dashboard.dashboard_page import DashboardPage

        return DashboardPage(self.driver)
