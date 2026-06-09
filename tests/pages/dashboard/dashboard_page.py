"""Dashboard page object for the Secure S3 File Portal."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

from tests.pages.base_page import BasePage

if TYPE_CHECKING:
    from tests.pages.audit_records.audit_log_page import AuditLogPage
    from tests.pages.login.login_page import LoginPage

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
    BUCKET_NAME: Locator = (By.CSS_SELECTOR, "[data-testid='bucket-name']")
    STORAGE_ENDPOINT: Locator = (By.CSS_SELECTOR, "[data-testid='storage-endpoint']")
    PORTAL_MODE: Locator = (By.CSS_SELECTOR, "[data-testid='portal-mode']")
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
    UPLOAD_LIMIT_NOTE: Locator = (By.CSS_SELECTOR, "[data-testid='upload-limit-note']")
    VIEWER_ROLE_PANEL: Locator = (By.CSS_SELECTOR, "[data-testid='viewer-role-panel']")
    FILES_PANEL: Locator = (By.CSS_SELECTOR, "[data-testid='files-panel']")
    FILES_TABLE: Locator = (By.CSS_SELECTOR, "[data-testid='files-table']")
    FILE_ROWS: Locator = (By.CSS_SELECTOR, "[data-testid='file-row']")
    FILE_NAME: Locator = (By.CSS_SELECTOR, "[data-testid='file-name']")
    FILE_OBJECT_KEY: Locator = (By.CSS_SELECTOR, "[data-testid='file-object-key']")
    FILE_UPLOADED_BY: Locator = (By.CSS_SELECTOR, "[data-testid='file-uploaded-by']")
    FILE_CONTENT_TYPE: Locator = (By.CSS_SELECTOR, "[data-testid='file-content-type']")
    FILE_UPLOADED_AT: Locator = (By.CSS_SELECTOR, "[data-testid='file-uploaded-at']")
    FILE_SIZE: Locator = (By.CSS_SELECTOR, "[data-testid='file-size']")
    DOWNLOAD_FILE_BUTTON: Locator = (
        By.CSS_SELECTOR,
        "[data-testid='download-file-button']",
    )
    DELETE_FILE_BUTTON: Locator = (
        By.CSS_SELECTOR,
        "[data-testid='delete-file-button']",
    )
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

    def get_page_heading_text(self) -> str:
        """
        Helper: return the dashboard page heading text.
        """
        return self.driver.find_element(*self.PAGE_HEADING).text.strip()

    def get_page_description_text(self) -> str:
        """
        Helper: return the dashboard page description text.
        """
        return self.driver.find_element(*self.PAGE_DESCRIPTION).text.strip()

    def get_bucket_name_text(self) -> str:
        """
        Helper: return the bucket name displayed in the dashboard.
        """
        return self.driver.find_element(*self.BUCKET_NAME).text.strip()

    def get_storage_endpoint_text(self) -> str:
        """
        Helper: return the storage endpoint displayed in the dashboard.
        """
        return self.driver.find_element(*self.STORAGE_ENDPOINT).text.strip()

    def get_portal_mode_text(self) -> str:
        """
        Helper: return the portal mode text displayed in the dashboard.
        """
        return self.driver.find_element(*self.PORTAL_MODE).text.strip()

    def get_upload_limit_note_text(self) -> str:
        """
        Helper: return the upload size note shown in the admin upload panel.
        """
        return self.driver.find_element(*self.UPLOAD_LIMIT_NOTE).text.strip()

    def get_flash_message_text(self) -> str:
        """
        Helper: return the visible dashboard flash message text.
        """
        return self.driver.find_element(*self.FLASH_MESSAGE).text.strip()

    def wait_for_flash_message_text(
        self,
        expected_text: str,
        timeout_seconds: int = 10,
    ) -> str:
        """
        Helper: wait until the dashboard flash message matches the expected text.
        """
        def _dashboard_flash_message_matches(driver) -> bool:
            try:
                flash_messages = driver.find_elements(*self.FLASH_MESSAGE)
                if not flash_messages:
                    return False

                return driver.find_element(*self.FLASH_MESSAGE).text.strip() == expected_text
            except StaleElementReferenceException:
                return False

        try:
            WebDriverWait(self.driver, timeout_seconds).until(
                _dashboard_flash_message_matches
            )
        except TimeoutException as exc:
            raise AssertionError(
                f"Expected dashboard flash message to become '{expected_text}' within "
                f"{timeout_seconds} seconds."
            ) from exc

        return self.get_flash_message_text()

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

    def is_files_panel_visible(self) -> bool:
        """
        Helper: return whether the main files panel is currently displayed.
        """
        panels = self.driver.find_elements(*self.FILES_PANEL)
        return bool(panels) and panels[0].is_displayed()

    def is_upload_submit_button_enabled(self) -> bool:
        """
        Helper: return whether the upload submit button is enabled and visible.
        """
        buttons = self.driver.find_elements(*self.UPLOAD_SUBMIT_BUTTON)
        return bool(buttons) and buttons[0].is_displayed() and buttons[0].is_enabled()

    def get_file_row_count(self) -> int:
        """
        Helper: return the number of visible file rows in the dashboard table.
        """
        return len(self.driver.find_elements(*self.FILE_ROWS))

    def get_visible_file_names(self) -> list[str]:
        """
        Helper: return the visible uploaded file names in table order.
        """
        return [
            element.text.strip()
            for element in self.driver.find_elements(*self.FILE_NAME)
        ]

    def contains_file_name(self, filename: str) -> bool:
        """
        Helper: return whether the dashboard currently shows the given file name.
        """
        return filename in self.get_visible_file_names()

    def wait_until_file_name_visible(
        self,
        filename: str,
        timeout_seconds: int = 10,
    ) -> bool:
        """
        Helper: wait until the dashboard shows the given file name.
        """
        WebDriverWait(self.driver, timeout_seconds).until(
            lambda _driver: self.contains_file_name(filename)
        )
        return self.contains_file_name(filename)

    def wait_until_file_name_not_visible(
        self,
        filename: str,
        timeout_seconds: int = 10,
    ) -> bool:
        """
        Helper: wait until the dashboard no longer shows the given file name.
        """
        WebDriverWait(self.driver, timeout_seconds).until(
            lambda _driver: not self.contains_file_name(filename)
        )
        return self.contains_file_name(filename) is False

    def get_selected_upload_file_name(self) -> str:
        """
        Helper: return the currently selected file name from the upload input.
        """
        raw_value = self.driver.find_element(*self.UPLOAD_INPUT).get_attribute("value")
        normalized_value = (raw_value or "").replace("\\", "/")
        return normalized_value.rsplit("/", maxsplit=1)[-1]

    def get_file_metadata_by_name(self, filename: str) -> dict[str, str]:
        """
        Helper: return the visible metadata for one uploaded file row.
        """
        row = self._find_file_row_by_name(filename)
        return {
            "filename": row.find_element(*self.FILE_NAME).text.strip(),
            "object_key": row.find_element(*self.FILE_OBJECT_KEY).text.strip(),
            "uploaded_by": row.find_element(*self.FILE_UPLOADED_BY).text.strip(),
            "content_type": row.find_element(*self.FILE_CONTENT_TYPE).text.strip(),
            "uploaded_at": row.find_element(*self.FILE_UPLOADED_AT).text.strip(),
            "size": row.find_element(*self.FILE_SIZE).text.strip(),
        }

    def is_empty_state_visible(self) -> bool:
        """
        Helper: return whether the empty-files state is currently displayed.
        """
        empty_states = self.driver.find_elements(*self.EMPTY_FILES_STATE)
        return bool(empty_states) and empty_states[0].is_displayed()

    def get_empty_state_text(self) -> str:
        """
        Helper: return the visible empty-files state message.
        """
        return self.driver.find_element(*self.EMPTY_FILES_STATE).text.strip()

    def _find_file_row_by_name(self, filename: str) -> WebElement:
        """
        Helper: return the file table row whose file-name cell matches the input.
        """
        for row in self.driver.find_elements(*self.FILE_ROWS):
            row_file_name = row.find_element(*self.FILE_NAME).text.strip()
            if row_file_name == filename:
                return row

        raise ValueError(f"Could not find a file row for '{filename}'.")

    # ### Action Methods ###

    def select_file_for_upload(self, file_path: str) -> None:
        """
        Select a local file in the dashboard upload input without submitting it.
        """
        self.driver.find_element(*self.UPLOAD_INPUT).send_keys(file_path)

    def submit_upload(self) -> None:
        """
        Submit the current dashboard upload form selection.
        """
        self.driver.find_element(*self.UPLOAD_SUBMIT_BUTTON).click()

    def upload_file(self, file_path: str) -> None:
        """
        Upload a file through the dashboard upload form.
        """
        self.select_file_for_upload(file_path)
        self.submit_upload()

    def drag_file_into_upload_input(self, file_path: str) -> None:
        """
        Simulate dragging a local file into the upload input without submitting it.
        """
        upload_input = self.driver.find_element(*self.UPLOAD_INPUT)

        self.driver.execute_script(
            """
            const existingInput = document.getElementById("__selenium_drag_source__");
            if (existingInput) {
                existingInput.remove();
            }

            const tempInput = document.createElement("input");
            tempInput.type = "file";
            tempInput.id = "__selenium_drag_source__";
            tempInput.style.position = "fixed";
            tempInput.style.left = "-9999px";
            document.body.appendChild(tempInput);
            """
        )
        temp_input = self.driver.find_element(By.ID, "__selenium_drag_source__")
        temp_input.send_keys(str(Path(file_path).resolve()))

        self.driver.execute_script(
            """
            const sourceInput = document.getElementById("__selenium_drag_source__");
            const targetInput = arguments[0];
            const dataTransfer = new DataTransfer();

            for (const file of sourceInput.files) {
                dataTransfer.items.add(file);
            }

            targetInput.files = dataTransfer.files;
            targetInput.dispatchEvent(new Event("input", { bubbles: true }));
            targetInput.dispatchEvent(new Event("change", { bubbles: true }));
            targetInput.dispatchEvent(
                new DragEvent("dragenter", { bubbles: true, dataTransfer })
            );
            targetInput.dispatchEvent(
                new DragEvent("dragover", { bubbles: true, dataTransfer })
            );
            targetInput.dispatchEvent(
                new DragEvent("drop", { bubbles: true, dataTransfer })
            );
            sourceInput.remove();
            """,
            upload_input,
        )

    def upload_file_by_drag_and_drop(self, file_path: str) -> None:
        """
        Simulate dragging a local file into the upload input, then submit it.
        """
        self.drag_file_into_upload_input(file_path)
        self.submit_upload()

    def click_download_file_by_name(self, filename: str) -> None:
        """
        Download the selected file from the dashboard table.
        """
        row = self._find_file_row_by_name(filename)
        download_button = row.find_element(*self.DOWNLOAD_FILE_BUTTON)
        self.driver.execute_script("arguments[0].click();", download_button)

    def click_delete_file_by_name(self, filename: str) -> None:
        """
        Delete the selected file from the dashboard table.
        """
        row = self._find_file_row_by_name(filename)
        delete_button = row.find_element(*self.DELETE_FILE_BUTTON)
        self.driver.execute_script("arguments[0].click();", delete_button)

    def click_audit_log_nav(self) -> AuditLogPage:
        """
        Open the audit log page from the top navigation.
        """
        # Runtime import stays local to avoid circular imports between page objects.
        from tests.pages.audit_records.audit_log_page import AuditLogPage

        self.driver.find_element(*self.AUDIT_LOG_NAV_LINK).click()
        return AuditLogPage(self.driver)

    def click_logout(self) -> LoginPage:
        """
        Log out from the dashboard and return the login page object.
        """
        # Runtime import stays local to avoid circular imports between page objects.
        from tests.pages.login.login_page import LoginPage

        self.driver.find_element(*self.LOGOUT_BUTTON).click()
        return LoginPage(self.driver)
