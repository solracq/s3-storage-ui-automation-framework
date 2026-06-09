"""
Curated smoke tests selected from the exploratory testing document.
"""

from __future__ import annotations

import pytest

from tests.pages.dashboard.dashboard_page import DashboardPage
from tests.pages.login.login_page import LoginPage
from tests.variables import (
    ADMIN_PASSWORD,
    ADMIN_ROLE,
    ADMIN_USERNAME,
    EMPTY_UPLOAD_MESSAGE,
    INVALID_LOGIN_MESSAGE,
    INVALID_PASSWORD,
    INVALID_USERNAME,
    LARGE_FILE_EXCEEDS_LIMIT_NAME,
    LARGE_FILE_EXCEEDS_LIMIT_PATH,
    LARGE_FILE_WITHIN_LIMIT_NAME,
    LARGE_FILE_WITHIN_LIMIT_PATH,
    OVERSIZE_UPLOAD_MESSAGE,
    PORTAL_BUCKET_NAME,
    PORTAL_MODE_TEXT,
    PORTAL_PAGE_DESCRIPTION_SNIPPET,
    PORTAL_PAGE_HEADING,
    PORTAL_STORAGE_ENDPOINT,
    STORAGE_STATUS_CONNECTED,
    UPLOAD_LIMIT_NOTE_TEXT,
    UPLOAD_SUCCESS_MESSAGE,
    VIEWER_PASSWORD,
    VIEWER_USERNAME,
)


def _sign_in_as_admin(driver, base_url: str) -> DashboardPage:
    """
    Sign in as the admin user and return the loaded dashboard page.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.

    Returns:
        DashboardPage: Loaded dashboard page for the signed-in admin user.
    """
    driver.get(base_url)
    login_page = LoginPage(driver)

    assert login_page.is_loaded(), (
        "Expected the login page to be displayed before admin sign-in."
    )

    dashboard_page = login_page.login_as_expected_success(
        ADMIN_USERNAME,
        ADMIN_PASSWORD,
    )

    assert dashboard_page.is_loaded(), (
        "Expected successful admin sign-in to land on the dashboard."
    )
    assert dashboard_page.get_current_user_text() == ADMIN_USERNAME, (
        f"Expected current dashboard user to be '{ADMIN_USERNAME}'."
    )
    assert dashboard_page.get_current_role_text() == ADMIN_ROLE, (
        f"Expected current dashboard role to be '{ADMIN_ROLE}'."
    )
    return dashboard_page


def _assert_invalid_login_combination(login_page: LoginPage, username: str, password: str) -> None:
    """
    Submit one invalid login attempt and verify the portal stays on the login page.

    Args:
        login_page: Login page object used for invalid credential submission.
        username: Username value to submit.
        password: Password value to submit.
    """
    login_page.login_as_expected_failure(username, password)

    assert login_page.is_loaded(), (
        "Expected the login page to remain visible after invalid credential submission."
    )
    assert (
        login_page.wait_for_flash_message_text(INVALID_LOGIN_MESSAGE) == INVALID_LOGIN_MESSAGE
    ), f"Expected invalid login message to be '{INVALID_LOGIN_MESSAGE}'."


@pytest.mark.smoke
@pytest.mark.usability
def test_open_portal_app_shows_core_admin_ui(driver, base_url: str, reset_portal_state) -> None:
    """
    Scenario 6 (from exploratory testing doc): Validate the main portal structure and core admin UI elements.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.
        reset_portal_state: Fixture that resets portal runtime state for isolation.
    """
    _ = reset_portal_state
    dashboard_page = _sign_in_as_admin(driver, base_url)

    assert dashboard_page.get_page_heading_text() == PORTAL_PAGE_HEADING, (
        f"Expected dashboard heading to be '{PORTAL_PAGE_HEADING}'."
    )
    assert PORTAL_PAGE_DESCRIPTION_SNIPPET in dashboard_page.get_page_description_text(), (
        "Expected dashboard description to explain the Phase 2 portal workflow context."
    )
    assert dashboard_page.get_storage_status_text() == STORAGE_STATUS_CONNECTED, (
        f"Expected storage status to show '{STORAGE_STATUS_CONNECTED}'."
    )
    assert dashboard_page.get_bucket_name_text() == PORTAL_BUCKET_NAME, (
        f"Expected bucket name to be '{PORTAL_BUCKET_NAME}'."
    )
    assert dashboard_page.get_storage_endpoint_text() == PORTAL_STORAGE_ENDPOINT, (
        f"Expected storage endpoint to be '{PORTAL_STORAGE_ENDPOINT}'."
    )
    assert dashboard_page.get_portal_mode_text() == PORTAL_MODE_TEXT, (
        f"Expected portal mode text to be '{PORTAL_MODE_TEXT}'."
    )
    assert dashboard_page.is_upload_panel_visible() is True, (
        "Expected the admin upload panel to be visible."
    )
    assert dashboard_page.get_upload_limit_note_text() == UPLOAD_LIMIT_NOTE_TEXT, (
        f"Expected upload limit note to be '{UPLOAD_LIMIT_NOTE_TEXT}'."
    )
    assert dashboard_page.get_selected_upload_file_name() == "", (
        "Expected no file to be selected in the upload input by default."
    )
    assert dashboard_page.is_upload_submit_button_enabled() is True, (
        "Expected the upload submit button to be visible and enabled."
    )
    assert dashboard_page.is_files_panel_visible() is True, (
        "Expected the Stored Files panel to be visible on the dashboard."
    )


@pytest.mark.smoke
@pytest.mark.negative
def test_upload_without_selecting_file_shows_error(driver, base_url: str, reset_portal_state, storage_service) -> None:
    """
    Scenario 16 (from exploratory testing doc): Validate the upload error path when no file is selected.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.
        reset_portal_state: Fixture that resets portal runtime state for isolation.
        storage_service: Storage service fixture used for backend object verification.
    """
    _ = reset_portal_state
    dashboard_page = _sign_in_as_admin(driver, base_url)

    dashboard_page.submit_upload()

    assert dashboard_page.wait_for_flash_message_text(EMPTY_UPLOAD_MESSAGE) == EMPTY_UPLOAD_MESSAGE, (
        f"Expected empty upload message to be '{EMPTY_UPLOAD_MESSAGE}'."
    )
    assert dashboard_page.is_empty_state_visible() is True, (
        "Expected the empty-files state to remain visible after failed empty upload."
    )
    assert dashboard_page.get_file_row_count() == 0, (
        "Expected no file rows to be displayed after failed empty upload."
    )
    assert storage_service.list_files() == [], (
        "Expected backend storage to remain empty after failed empty upload."
    )


@pytest.mark.smoke
@pytest.mark.negative
def test_large_file_over_limit_is_rejected(driver, base_url: str, reset_portal_state, storage_service) -> None:
    """
    Scenario 18 (from exploratory testing doc) : Validate rejection of files that exceed the 1 MB upload limit.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.
        reset_portal_state: Fixture that resets portal runtime state for isolation.
        storage_service: Storage service fixture used for backend object verification.
    """
    _ = reset_portal_state
    dashboard_page = _sign_in_as_admin(driver, base_url)

    dashboard_page.upload_file(str(LARGE_FILE_EXCEEDS_LIMIT_PATH))

    assert dashboard_page.wait_for_flash_message_text(OVERSIZE_UPLOAD_MESSAGE) == OVERSIZE_UPLOAD_MESSAGE, (
        f"Expected oversize upload message to be '{OVERSIZE_UPLOAD_MESSAGE}'."
    )
    assert dashboard_page.contains_file_name(LARGE_FILE_EXCEEDS_LIMIT_NAME) is False, (
        f"Expected '{LARGE_FILE_EXCEEDS_LIMIT_NAME}' not to appear after failed upload."
    )
    assert dashboard_page.is_empty_state_visible() is True, (
        "Expected the empty-files state to remain visible after oversize upload rejection."
    )
    assert storage_service.list_files() == [], (
        "Expected backend storage to remain empty after oversize upload rejection."
    )


@pytest.mark.smoke
@pytest.mark.edge
def test_large_file_within_limit_uploads_successfully(driver, base_url: str, reset_portal_state, storage_service) -> None:
    """
    Scenario 22 (from exploratory testing doc): Validate successful upload of a large file that remains within the limit.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.
        reset_portal_state: Fixture that resets portal runtime state for isolation.
        storage_service: Storage service fixture used for backend object verification.
    """
    _ = reset_portal_state
    dashboard_page = _sign_in_as_admin(driver, base_url)

    dashboard_page.upload_file(str(LARGE_FILE_WITHIN_LIMIT_PATH))

    assert dashboard_page.wait_for_flash_message_text(UPLOAD_SUCCESS_MESSAGE) == UPLOAD_SUCCESS_MESSAGE, (
        f"Expected upload success message to be '{UPLOAD_SUCCESS_MESSAGE}'."
    )
    assert dashboard_page.wait_until_file_name_visible(LARGE_FILE_WITHIN_LIMIT_NAME) is True, (
        f"Expected '{LARGE_FILE_WITHIN_LIMIT_NAME}' to appear after successful upload."
    )
    assert dashboard_page.get_file_metadata_by_name(LARGE_FILE_WITHIN_LIMIT_NAME)["size"] != "", (
        "Expected the uploaded near-limit file to show a visible size value."
    )
    backend_file_names = [stored_file.filename for stored_file in storage_service.list_files()]
    assert LARGE_FILE_WITHIN_LIMIT_NAME in backend_file_names, (
        f"Expected backend storage to contain '{LARGE_FILE_WITHIN_LIMIT_NAME}'."
    )


@pytest.mark.smoke
@pytest.mark.authentication
def test_admin_invalid_login_combinations_are_rejected(driver, base_url: str, reset_portal_state) -> None:
    """
    Scenario 24 (from exploratory testing doc): Validate that invalid admin credential combinations are denied.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.
        reset_portal_state: Fixture that resets portal runtime state for isolation.
    """
    _ = reset_portal_state
    driver.get(base_url)

    login_page = LoginPage(driver)

    assert login_page.is_loaded(), (
        "Expected the login page to be displayed before admin invalid login attempts."
    )

    _assert_invalid_login_combination(
        login_page,
        ADMIN_USERNAME,
        INVALID_PASSWORD,
    )
    _assert_invalid_login_combination(
        login_page,
        INVALID_USERNAME,
        ADMIN_PASSWORD,
    )


@pytest.mark.smoke
@pytest.mark.authentication
def test_viewer_invalid_login_combinations_are_rejected(driver, base_url: str, reset_portal_state) -> None:
    """
    Scenario 25 (from exploratory testing doc): Validate that invalid viewer credential combinations are denied.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.
        reset_portal_state: Fixture that resets portal runtime state for isolation.
    """
    _ = reset_portal_state
    driver.get(base_url)

    login_page = LoginPage(driver)

    assert login_page.is_loaded(), (
        "Expected the login page to be displayed before viewer invalid login attempts."
    )

    _assert_invalid_login_combination(
        login_page,
        VIEWER_USERNAME,
        INVALID_PASSWORD,
    )
    _assert_invalid_login_combination(
        login_page,
        INVALID_USERNAME,
        VIEWER_PASSWORD,
    )
