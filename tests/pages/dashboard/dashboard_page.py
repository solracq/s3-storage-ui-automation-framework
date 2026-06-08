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
    PAGE_DESCRIPTION: Locator = (By.CSS_SELECTOR, "[data-testid='page-description']")
    FLASH_MESSAGE: Locator = (By.CSS_SELECTOR, "[data-testid='flash-message']")
    STORAGE_STATUS_PANEL: Locator = (
        By.CSS_SELECTOR,
        "[data-testid='storage-status-panel']",
    )
    STORAGE_STATUS: Locator = (By.CSS_SELECTOR, "[data-testid='storage-status']")
    CURRENT_PORTAL_USER: Locator = (
        By.CSS_SELECTOR,
        "[data-testid='current-portal-user']",
    )
    CURRENT_PORTAL_ROLE: Locator = (
        By.CSS_SELECTOR,
        "[data-testid='current-portal-role']",
    )
    UPLOAD_PANEL: Locator = (By.CSS_SELECTOR, "[data-testid='upload-panel']")
    UPLOAD_INPUT: Locator = (By.CSS_SELECTOR, "[data-testid='upload-input']")
    UPLOAD_SUBMIT_BUTTON: Locator = (
        By.CSS_SELECTOR,
        "[data-testid='upload-submit-button']",
    )
    VIEWER_ROLE_PANEL: Locator = (By.CSS_SELECTOR, "[data-testid='viewer-role-panel']")
    FILES_PANEL: Locator = (By.CSS_SELECTOR, "[data-testid='files-panel']")
    FILES_TABLE: Locator = (By.CSS_SELECTOR, "[data-testid='files-table']")
    EMPTY_FILES_STATE: Locator = (
        By.CSS_SELECTOR,
        "[data-testid='empty-files-state']",
    )
    AUDIT_LOG_NAV_LINK: Locator = (By.CSS_SELECTOR, "[data-testid='nav-audit-link']")
    LOGOUT_BUTTON: Locator = (By.CSS_SELECTOR, "[data-testid='logout-button']")

    # ### Helper Methods ###

    def is_loaded(self) -> bool:
        """
        Helper: return whether the main dashboard elements are present and visible.
        """
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

    def get_storage_status_text(self) -> str:
        """
        Helper: return the storage status text shown in the dashboard.
        """
        return self.driver.find_element(*self.STORAGE_STATUS).text.strip()

    def get_flash_message_text(self) -> str:
        """
        Helper: return the visible dashboard flash message text.
        """
        return self.driver.find_element(*self.FLASH_MESSAGE).text.strip()

    def get_current_user_text(self) -> str:
        """
        Helper: return the signed-in user shown in the dashboard.
        """
        return self.driver.find_element(*self.CURRENT_PORTAL_USER).text.strip()

    def get_current_role_text(self) -> str:
        """
        Helper: return the signed-in user's role shown in the dashboard.
        """
        return self.driver.find_element(*self.CURRENT_PORTAL_ROLE).text.strip()

    def is_upload_panel_visible(self) -> bool:
        """
        Helper: return whether the upload panel is currently displayed.
        """
        upload_panels = self.driver.find_elements(*self.UPLOAD_PANEL)
        return bool(upload_panels) and upload_panels[0].is_displayed()

    def is_viewer_role_panel_visible(self) -> bool:
        """
        Helper: return whether the viewer role panel is currently displayed.
        """
        viewer_panels = self.driver.find_elements(*self.VIEWER_ROLE_PANEL)
        return bool(viewer_panels) and viewer_panels[0].is_displayed()

    def has_files_table(self) -> bool:
        """
        Helper: return whether the files table is currently displayed.
        """
        tables = self.driver.find_elements(*self.FILES_TABLE)
        return bool(tables) and tables[0].is_displayed()

    def is_empty_state_visible(self) -> bool:
        """
        Helper: return whether the empty-files state is currently displayed.
        """
        empty_states = self.driver.find_elements(*self.EMPTY_FILES_STATE)
        return bool(empty_states) and empty_states[0].is_displayed()

    # ### Action Methods ###

    def upload_file(self, file_path: str) -> None:
        """
        Upload a file through the dashboard upload form.
        """
        self.driver.find_element(*self.UPLOAD_INPUT).send_keys(file_path)
        self.driver.find_element(*self.UPLOAD_SUBMIT_BUTTON).click()

    def click_audit_log_nav(self) -> "AuditLogPage":
        """
        Open the audit log page from the top navigation.
        """
        from tests.pages.audit_records.audit_log_page import AuditLogPage

        self.driver.find_element(*self.AUDIT_LOG_NAV_LINK).click()
        return AuditLogPage(self.driver)

    def click_logout(self) -> "LoginPage":
        """
        Log out from the dashboard and return the login page object.
        """
        from tests.pages.login.login_page import LoginPage

        self.driver.find_element(*self.LOGOUT_BUTTON).click()
        return LoginPage(self.driver)
