"""Audit log page object for the Secure S3 File Portal."""

from __future__ import annotations

from selenium.webdriver.common.by import By

from tests.pages.dashboard.dashboard_page import DashboardPage
from tests.pages.login.login_page import LoginPage
from tests.pages.base_page import BasePage

Locator = tuple[str, str]


class AuditLogPage(BasePage):
    """Represent the admin audit log page."""

    URL_PATH = "/audit-logs"

    PAGE_HERO: Locator = (By.CSS_SELECTOR, "[data-testid='audit-hero']")
    PAGE_HEADING: Locator = (By.CSS_SELECTOR, "[data-testid='audit-heading']")
    PAGE_DESCRIPTION: Locator = (By.CSS_SELECTOR, "[data-testid='audit-description']")
    AUDIT_LOG_PANEL: Locator = (By.CSS_SELECTOR, "[data-testid='audit-log-panel']")
    AUDIT_TABLE: Locator = (By.CSS_SELECTOR, "[data-testid='audit-table']")
    AUDIT_ROWS: Locator = (By.CSS_SELECTOR, "[data-testid='audit-row']")
    AUDIT_EVENT_TYPES: Locator = (By.CSS_SELECTOR, "[data-testid='audit-event-type']")
    AUDIT_OUTCOMES: Locator = (By.CSS_SELECTOR, "[data-testid='audit-outcome']")
    AUDIT_DETAILS: Locator = (By.CSS_SELECTOR, "[data-testid='audit-details']")
    EMPTY_AUDIT_STATE: Locator = (By.CSS_SELECTOR, "[data-testid='empty-audit-state']")
    DASHBOARD_NAV_LINK: Locator = (
        By.CSS_SELECTOR,
        "[data-testid='nav-dashboard-link']",
    )
    LOGOUT_BUTTON: Locator = (By.CSS_SELECTOR, "[data-testid='logout-button']")

    # ### Helper Methods ###

    def is_loaded(self) -> bool:
        """
        Helper: return whether the main audit log page elements are present and visible.
        """
        page_hero = self.driver.find_elements(*self.PAGE_HERO)
        headings = self.driver.find_elements(*self.PAGE_HEADING)
        audit_panels = self.driver.find_elements(*self.AUDIT_LOG_PANEL)

        if not page_hero or not headings or not audit_panels:
            return False

        return (
            page_hero[0].is_displayed()
            and headings[0].is_displayed()
            and audit_panels[0].is_displayed()
        )

    def has_audit_table(self) -> bool:
        """
        Helper: return whether the audit table is currently displayed.
        """
        tables = self.driver.find_elements(*self.AUDIT_TABLE)
        return bool(tables) and tables[0].is_displayed()

    def is_empty_audit_state_visible(self) -> bool:
        """
        Helper: return whether the empty audit state is currently displayed.
        """
        empty_states = self.driver.find_elements(*self.EMPTY_AUDIT_STATE)
        return bool(empty_states) and empty_states[0].is_displayed()

    def get_audit_row_count(self) -> int:
        """
        Helper: return the number of visible audit rows.
        """
        return len(self.driver.find_elements(*self.AUDIT_ROWS))

    def get_visible_event_types(self) -> list[str]:
        """
        Helper: return the visible audit event types in table order.
        """
        return [
            element.text.strip()
            for element in self.driver.find_elements(*self.AUDIT_EVENT_TYPES)
        ]

    def contains_event_type(self, event_type: str) -> bool:
        """
        Helper: return whether the audit table shows the given event type.
        """
        return event_type in self.get_visible_event_types()

    # ### Action Methods ###

    def click_dashboard_nav(self) -> "DashboardPage":
        """
        Open the dashboard page from the top navigation.
        """
        self.driver.find_element(*self.DASHBOARD_NAV_LINK).click()
        return DashboardPage(self.driver)

    def click_logout(self) -> "LoginPage":
        """
        Log out from the audit log page and return the login page object.
        """
        self.driver.find_element(*self.LOGOUT_BUTTON).click()
        return LoginPage(self.driver)
