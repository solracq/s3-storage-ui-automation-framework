"""
Regression coverage for portal usability, clarity, and page structure scenarios.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from tests.pages.dashboard.dashboard_page import DashboardPage
from tests.pages.login.login_page import LoginPage
from tests.variables import (
    ADMIN_PASSWORD,
    ADMIN_ROLE,
    ADMIN_USERNAME,
    EMPTY_FILES_MESSAGE,
    PNG_CONTENT_TYPE,
    PNG_FILE_NAME,
    PNG_FILE_PATH,
    PORTAL_BUCKET_NAME,
    SMALL_TEXT_FILE_NAME,
    SMALL_TEXT_FILE_PATH,
    STORAGE_STATUS_CONNECTED,
    TEXT_PLAIN_CONTENT_TYPE,
    UPLOAD_LIMIT_NOTE_TEXT,
    UPLOAD_SUCCESS_MESSAGE,
    VIEWER_PASSWORD,
    VIEWER_ROLE,
    VIEWER_ROLE_STATUS_TEXT,
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
    return dashboard_page


def _sign_in_as_viewer(driver, base_url: str) -> DashboardPage:
    """
    Sign in as the viewer user and return the loaded dashboard page.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.

    Returns:
        DashboardPage: Loaded dashboard page for the signed-in viewer user.
    """
    driver.get(base_url)
    login_page = LoginPage(driver)

    assert login_page.is_loaded(), (
        "Expected the login page to be displayed before viewer sign-in."
    )

    dashboard_page = login_page.login_as_expected_success(
        VIEWER_USERNAME,
        VIEWER_PASSWORD,
    )

    assert dashboard_page.is_loaded(), (
        "Expected successful viewer sign-in to land on the dashboard."
    )
    return dashboard_page


def _upload_file_and_wait(
    dashboard_page: DashboardPage,
    file_path: Path,
    expected_filename: str,
) -> dict[str, str]:
    """
    Upload one file and wait until the dashboard reflects the new row.

    Args:
        dashboard_page: Dashboard page object used for the upload workflow.
        file_path: Local file path to upload.
        expected_filename: Expected filename to appear in the Stored Files table.

    Returns:
        dict[str, str]: Visible metadata for the uploaded file row.
    """
    dashboard_page.upload_file(str(file_path))

    assert (
        dashboard_page.wait_for_flash_message_text(UPLOAD_SUCCESS_MESSAGE)
        == UPLOAD_SUCCESS_MESSAGE
    ), f"Expected upload success message to be '{UPLOAD_SUCCESS_MESSAGE}'."
    assert dashboard_page.wait_until_file_name_visible(expected_filename) is True, (
        f"Expected '{expected_filename}' to appear in the Stored Files section."
    )

    return dashboard_page.get_file_metadata_by_name(expected_filename)


def _format_size_label(size_bytes: int) -> str:
    """
    Format a file size the same way the portal UI currently displays it.

    Args:
        size_bytes: Raw file size in bytes.

    Returns:
        str: Human-readable size label expected in the UI.
    """
    units = ["B", "KB", "MB", "GB"]
    size = float(size_bytes)
    unit_index = 0

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"

    return f"{size:.1f} {units[unit_index]}"


@pytest.mark.regression
@pytest.mark.usability
def test_initial_stored_files_status_is_empty(driver, base_url: str, reset_portal_state, storage_service) -> None:
    """
    Scenario 7 (from exploratory testing doc): Verify the initial Stored Files status when no objects exist.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.
        reset_portal_state: Fixture that resets portal runtime state for isolation.
        storage_service: Storage service fixture used for backend object verification.
    """
    _ = reset_portal_state
    dashboard_page = _sign_in_as_admin(driver, base_url)

    assert dashboard_page.is_empty_state_visible() is True, (
        "Expected the empty-files state to be visible when no files exist."
    )
    assert dashboard_page.get_empty_state_text() == EMPTY_FILES_MESSAGE, (
        f"Expected empty-files message to be '{EMPTY_FILES_MESSAGE}'."
    )
    assert dashboard_page.get_file_row_count() == 0, (
        "Expected no file rows to be displayed in the empty initial state."
    )
    assert storage_service.list_files() == [], (
        "Expected backend storage to remain empty in the initial state."
    )


@pytest.mark.regression
@pytest.mark.usability
def test_uploaded_file_name_matches_actual_file_name(driver, base_url: str, reset_portal_state) -> None:
    """
    Scenario 8 (from exploratory testing doc): Verify that the uploaded file name and extension match the source file.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.
        reset_portal_state: Fixture that resets portal runtime state for isolation.
    """
    _ = reset_portal_state
    dashboard_page = _sign_in_as_admin(driver, base_url)
    uploaded_file_metadata = _upload_file_and_wait(
        dashboard_page,
        SMALL_TEXT_FILE_PATH,
        SMALL_TEXT_FILE_NAME,
    )

    assert uploaded_file_metadata["filename"] == SMALL_TEXT_FILE_NAME, (
        f"Expected visible file name to be '{SMALL_TEXT_FILE_NAME}'."
    )


@pytest.mark.regression
@pytest.mark.usability
def test_uploaded_object_key_has_expected_structure(driver, base_url: str, reset_portal_state) -> None:
    """
    Scenario 9 (from exploratory testing doc): Verify that the uploaded object key follows the expected format.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.
        reset_portal_state: Fixture that resets portal runtime state for isolation.
    """
    _ = reset_portal_state
    dashboard_page = _sign_in_as_admin(driver, base_url)
    uploaded_file_metadata = _upload_file_and_wait(
        dashboard_page,
        SMALL_TEXT_FILE_PATH,
        SMALL_TEXT_FILE_NAME,
    )

    object_key = uploaded_file_metadata["object_key"]

    assert object_key.startswith("portal-uploads/"), (
        "Expected uploaded object key to start with 'portal-uploads/'."
    )
    assert re.fullmatch(
        r"portal-uploads/\d{8}T\d{6}Z-[0-9a-f]{8}-small_file\.txt",
        object_key,
    ), (
        "Expected uploaded object key to contain the upload folder, UTC timestamp, "
        "random suffix, and original file name."
    )


@pytest.mark.regression
@pytest.mark.usability
def test_uploaded_by_matches_current_signed_in_user(driver, base_url: str, reset_portal_state) -> None:
    """
    Scenario 10 (from exploratory testing doc): Verify that the uploaded-by column matches the signed-in admin user.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.
        reset_portal_state: Fixture that resets portal runtime state for isolation.
    """
    _ = reset_portal_state
    dashboard_page = _sign_in_as_admin(driver, base_url)
    uploaded_file_metadata = _upload_file_and_wait(
        dashboard_page,
        SMALL_TEXT_FILE_PATH,
        SMALL_TEXT_FILE_NAME,
    )

    assert uploaded_file_metadata["uploaded_by"] == ADMIN_USERNAME, (
        f"Expected uploaded-by value to be '{ADMIN_USERNAME}'."
    )


@pytest.mark.regression
@pytest.mark.usability
def test_uploaded_content_types_match_text_and_image_files(driver, base_url: str, reset_portal_state) -> None:
    """
    Scenario 11 (from exploratory testing doc): Verify that text and image uploads display the correct content types.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.
        reset_portal_state: Fixture that resets portal runtime state for isolation.
    """
    _ = reset_portal_state
    dashboard_page = _sign_in_as_admin(driver, base_url)

    text_file_metadata = _upload_file_and_wait(
        dashboard_page,
        SMALL_TEXT_FILE_PATH,
        SMALL_TEXT_FILE_NAME,
    )
    png_file_metadata = _upload_file_and_wait(
        dashboard_page,
        PNG_FILE_PATH,
        PNG_FILE_NAME,
    )

    assert text_file_metadata["content_type"] == TEXT_PLAIN_CONTENT_TYPE, (
        f"Expected text file content type to be '{TEXT_PLAIN_CONTENT_TYPE}'."
    )
    assert png_file_metadata["content_type"] == PNG_CONTENT_TYPE, (
        f"Expected image file content type to be '{PNG_CONTENT_TYPE}'."
    )


@pytest.mark.regression
@pytest.mark.usability
def test_ploaded_at_uses_expected_timestamp_format(driver, base_url: str, reset_portal_state) -> None:
    """
    Scenario 12 (from exploratory testing doc): Verify that the uploaded-at column uses the expected timestamp format.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.
        reset_portal_state: Fixture that resets portal runtime state for isolation.
    """
    _ = reset_portal_state
    dashboard_page = _sign_in_as_admin(driver, base_url)
    uploaded_file_metadata = _upload_file_and_wait(
        dashboard_page,
        SMALL_TEXT_FILE_PATH,
        SMALL_TEXT_FILE_NAME,
    )

    assert re.fullmatch(
        r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} UTC",
        uploaded_file_metadata["uploaded_at"],
    ), (
        "Expected uploaded-at value to follow the format 'YYYY-MM-DD HH:MM:SS UTC'."
    )


@pytest.mark.regression
@pytest.mark.usability
def test_uploaded_size_matches_actual_file_size(driver, base_url: str, reset_portal_state) -> None:
    """
    Scenario 13 (from exploratory testing doc): Verify that the visible size value matches the uploaded file size.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.
        reset_portal_state: Fixture that resets portal runtime state for isolation.
    """
    _ = reset_portal_state
    dashboard_page = _sign_in_as_admin(driver, base_url)
    uploaded_file_metadata = _upload_file_and_wait(
        dashboard_page,
        SMALL_TEXT_FILE_PATH,
        SMALL_TEXT_FILE_NAME,
    )

    expected_size_label = _format_size_label(SMALL_TEXT_FILE_PATH.stat().st_size)

    assert uploaded_file_metadata["size"] == expected_size_label, (
        f"Expected visible size label to be '{expected_size_label}'."
    )


@pytest.mark.regression
@pytest.mark.usability
def test_uploaded_file_actions_are_visible_and_clickable(driver, base_url: str, reset_portal_state) -> None:
    """
    Scenario 14 (from exploratory testing doc): Verify that the admin sees Download and Delete actions for uploaded files.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.
        reset_portal_state: Fixture that resets portal runtime state for isolation.
    """
    _ = reset_portal_state
    dashboard_page = _sign_in_as_admin(driver, base_url)
    _upload_file_and_wait(
        dashboard_page,
        SMALL_TEXT_FILE_PATH,
        SMALL_TEXT_FILE_NAME,
    )

    assert dashboard_page.is_download_action_visible_for_file(SMALL_TEXT_FILE_NAME) is True, (
        "Expected the Download action to be visible for the uploaded file."
    )
    assert dashboard_page.is_download_action_clickable_for_file(SMALL_TEXT_FILE_NAME) is True, (
        "Expected the Download action to be clickable for the uploaded file."
    )
    assert dashboard_page.is_delete_action_visible_for_file(SMALL_TEXT_FILE_NAME) is True, (
        "Expected the Delete action to be visible for the uploaded file."
    )
    assert dashboard_page.is_delete_action_clickable_for_file(SMALL_TEXT_FILE_NAME) is True, (
        "Expected the Delete action to be clickable for the uploaded file."
    )


@pytest.mark.regression
@pytest.mark.usability
def test_uploaded_file_persists_after_refresh_and_disappears_after_delete_refresh(driver, base_url: str, reset_portal_state) -> None:
    """
    Scenario 15 (from exploratory testing doc): Verify refresh behavior after upload and after delete.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.
        reset_portal_state: Fixture that resets portal runtime state for isolation.
    """
    _ = reset_portal_state
    dashboard_page = _sign_in_as_admin(driver, base_url)
    uploaded_file_metadata = _upload_file_and_wait(
        dashboard_page,
        SMALL_TEXT_FILE_PATH,
        SMALL_TEXT_FILE_NAME,
    )

    driver.refresh()

    assert dashboard_page.wait_until_file_name_visible(SMALL_TEXT_FILE_NAME) is True, (
        f"Expected '{SMALL_TEXT_FILE_NAME}' to remain visible after refresh."
    )
    refreshed_file_metadata = dashboard_page.get_file_metadata_by_name(
        SMALL_TEXT_FILE_NAME
    )

    assert refreshed_file_metadata["object_key"] == uploaded_file_metadata["object_key"], (
        "Expected the same uploaded object key to remain visible after refresh."
    )

    dashboard_page.click_delete_file_by_name(SMALL_TEXT_FILE_NAME)

    driver.refresh()

    assert dashboard_page.wait_until_file_name_not_visible(SMALL_TEXT_FILE_NAME) is True, (
        f"Expected '{SMALL_TEXT_FILE_NAME}' to be gone after delete and refresh."
    )
    assert dashboard_page.is_empty_state_visible() is True, (
        "Expected the empty-files state to be visible after deleting the only file."
    )


@pytest.mark.regression
@pytest.mark.usability
def test_admin_role_sees_expected_buttons_links_badges_and_text(driver, base_url: str, reset_portal_state) -> None:
    """
    Scenario 27 (from exploratory testing doc): Verify the admin role sees the expected controls and descriptive text.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.
        reset_portal_state: Fixture that resets portal runtime state for isolation.
    """
    _ = reset_portal_state
    dashboard_page = _sign_in_as_admin(driver, base_url)
    _upload_file_and_wait(
        dashboard_page,
        SMALL_TEXT_FILE_PATH,
        SMALL_TEXT_FILE_NAME,
    )

    assert dashboard_page.is_topbar_visible() is True, (
        "Expected the shared portal top bar to be visible for the admin role."
    )
    assert dashboard_page.is_dashboard_nav_visible() is True, (
        "Expected the Dashboard navigation link to be visible for the admin role."
    )
    assert dashboard_page.is_audit_log_nav_visible() is True, (
        "Expected the Audit Log navigation link to be visible for the admin role."
    )
    assert dashboard_page.is_current_user_badge_visible() is True, (
        "Expected the current-user badge to be visible for the admin role."
    )
    assert ADMIN_USERNAME in dashboard_page.get_current_user_badge_text(), (
        f"Expected the current-user badge to contain '{ADMIN_USERNAME}'."
    )
    assert ADMIN_ROLE in dashboard_page.get_current_user_badge_text(), (
        f"Expected the current-user badge to contain '{ADMIN_ROLE}'."
    )
    assert dashboard_page.is_logout_button_visible() is True, (
        "Expected the Logout button to be visible for the admin role."
    )
    assert dashboard_page.is_upload_panel_visible() is True, (
        "Expected the Upload File panel to be visible for the admin role."
    )
    assert dashboard_page.get_upload_limit_note_text() == UPLOAD_LIMIT_NOTE_TEXT, (
        f"Expected upload limit note to be '{UPLOAD_LIMIT_NOTE_TEXT}'."
    )
    assert dashboard_page.is_download_action_visible_for_file(SMALL_TEXT_FILE_NAME) is True, (
        "Expected the Download action to be visible for the admin role."
    )
    assert dashboard_page.is_delete_action_visible_for_file(SMALL_TEXT_FILE_NAME) is True, (
        "Expected the Delete action to be visible for the admin role."
    )
    assert dashboard_page.get_current_user_text() == ADMIN_USERNAME, (
        f"Expected dashboard current user text to be '{ADMIN_USERNAME}'."
    )
    assert dashboard_page.get_current_role_text() == ADMIN_ROLE, (
        f"Expected dashboard current role text to be '{ADMIN_ROLE}'."
    )


@pytest.mark.regression
@pytest.mark.usability
def test_viewer_role_sees_only_allowed_buttons_links_badges_and_text(driver, base_url: str, reset_portal_state) -> None:
    """
    Scenario 28 (from exploratory testing doc): Verify the viewer role sees only the controls allowed for download-only access.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.
        reset_portal_state: Fixture that resets portal runtime state for isolation.
    """
    _ = reset_portal_state
    admin_dashboard_page = _sign_in_as_admin(driver, base_url)
    _upload_file_and_wait(
        admin_dashboard_page,
        SMALL_TEXT_FILE_PATH,
        SMALL_TEXT_FILE_NAME,
    )
    login_page = admin_dashboard_page.click_logout()

    assert login_page.is_loaded(), (
        "Expected logout to return the browser to the login page before viewer sign-in."
    )

    viewer_dashboard_page = _sign_in_as_viewer(driver, base_url)

    assert viewer_dashboard_page.is_topbar_visible() is True, (
        "Expected the shared portal top bar to be visible for the viewer role."
    )
    assert viewer_dashboard_page.is_dashboard_nav_visible() is True, (
        "Expected the Dashboard navigation link to be visible for the viewer role."
    )
    assert viewer_dashboard_page.is_audit_log_nav_visible() is False, (
        "Expected the Audit Log navigation link not to be visible for the viewer role."
    )
    assert viewer_dashboard_page.is_current_user_badge_visible() is True, (
        "Expected the current-user badge to be visible for the viewer role."
    )
    assert VIEWER_USERNAME in viewer_dashboard_page.get_current_user_badge_text(), (
        f"Expected the current-user badge to contain '{VIEWER_USERNAME}'."
    )
    assert VIEWER_ROLE in viewer_dashboard_page.get_current_user_badge_text(), (
        f"Expected the current-user badge to contain '{VIEWER_ROLE}'."
    )
    assert viewer_dashboard_page.is_logout_button_visible() is True, (
        "Expected the Logout button to be visible for the viewer role."
    )
    assert viewer_dashboard_page.is_viewer_role_panel_visible() is True, (
        "Expected the Viewer Access panel to be visible for the viewer role."
    )
    assert viewer_dashboard_page.is_upload_panel_visible() is False, (
        "Expected the Upload File panel not to be visible for the viewer role."
    )
    assert viewer_dashboard_page.get_viewer_role_status_text() == VIEWER_ROLE_STATUS_TEXT, (
        f"Expected viewer status text to be '{VIEWER_ROLE_STATUS_TEXT}'."
    )
    assert viewer_dashboard_page.is_download_action_visible_for_file(SMALL_TEXT_FILE_NAME) is True, (
        "Expected the Download action to be visible for the viewer role."
    )
    assert viewer_dashboard_page.is_delete_action_visible_for_file(SMALL_TEXT_FILE_NAME) is False, (
        "Expected the Delete action not to be visible for the viewer role."
    )
    assert viewer_dashboard_page.get_current_user_text() == VIEWER_USERNAME, (
        f"Expected dashboard current user text to be '{VIEWER_USERNAME}'."
    )
    assert viewer_dashboard_page.get_current_role_text() == VIEWER_ROLE, (
        f"Expected dashboard current role text to be '{VIEWER_ROLE}'."
    )
