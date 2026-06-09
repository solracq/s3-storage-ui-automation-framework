"""
Smoke tests for critical Secure S3 File Portal happy-path workflows.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from urllib.request import urlopen

import pytest

from tests.pages.dashboard.dashboard_page import DashboardPage
from tests.pages.login.login_page import LoginPage
from tests.variables import (
    ADMIN_PASSWORD,
    ADMIN_USERNAME,
    DELETE_SUCCESS_MESSAGE,
    HEALTH_STATUS_OK,
    PNG_FILE_NAME,
    PNG_FILE_PATH,
    PORTAL_BUCKET_NAME,
    SMALL_TEXT_FILE_NAME,
    SMALL_TEXT_FILE_PATH,
    STORAGE_STATUS_CONNECTED,
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


def _wait_for_download(
    download_directory: Path,
    expected_filename: str,
    *,
    timeout_seconds: int = 10,
) -> Path:
    """
    Wait until the expected downloaded file appears in the browser download folder.

    Args:
        download_directory: Temporary browser download directory for the current test.
        expected_filename: File name expected to appear after the download action.
        timeout_seconds: Maximum wait time before failing the download verification.

    Returns:
        Path: Downloaded file path once the browser finishes writing it.
    """
    deadline = time.monotonic() + timeout_seconds

    while time.monotonic() < deadline:
        completed_downloads = [
            file_path
            for file_path in download_directory.iterdir()
            if file_path.is_file() and not file_path.name.endswith(".crdownload")
        ]
        exact_match = next(
            (
                file_path
                for file_path in completed_downloads
                if file_path.name == expected_filename
            ),
            None,
        )

        if exact_match is not None and exact_match.stat().st_size > 0:
            return exact_match

        if completed_downloads:
            most_recent_download = max(
                completed_downloads,
                key=lambda file_path: file_path.stat().st_mtime,
            )
            if most_recent_download.stat().st_size > 0:
                return most_recent_download

        time.sleep(0.25)

    raise AssertionError(
        f"Expected downloaded file '{expected_filename}' to appear in "
        f"'{download_directory}' within {timeout_seconds} seconds."
    )


@pytest.mark.smoke
def test_portal_health_endpoint_reports_ready_status(base_url: str) -> None:
    """
    Verify the portal health endpoint reports an operational ready state.

    Args:
        base_url: Base portal URL used to open the application under test.
    """
    with urlopen(f"{base_url}/health") as response:
        health_payload = json.loads(response.read().decode("utf-8"))
        response_status_code = response.status

    assert response_status_code == 200, (
        "Expected the portal health endpoint to return HTTP 200."
    )
    assert health_payload["status"] == HEALTH_STATUS_OK, (
        f"Expected health endpoint status to be '{HEALTH_STATUS_OK}'."
    )
    assert health_payload["storage_ready"] is True, (
        "Expected health endpoint storage readiness to be True."
    )
    assert health_payload["bucket"] == PORTAL_BUCKET_NAME, (
        f"Expected health endpoint bucket to be '{PORTAL_BUCKET_NAME}'."
    )
    assert health_payload["storage_error"] is None, (
        "Expected health endpoint storage_error to be None."
    )


@pytest.mark.smoke
def test_admin_can_upload_file_by_selecting_it(
    driver,
    base_url: str,
    reset_portal_state,
    storage_service,
) -> None:
    """
    Verify the admin user can upload a file by selecting it from the upload input.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.
        reset_portal_state: Fixture that resets portal runtime state for isolation.
        storage_service: Storage service fixture used for backend object verification.
    """
    _ = reset_portal_state
    dashboard_page = _sign_in_as_admin(driver, base_url)

    assert dashboard_page.get_storage_status_text() == STORAGE_STATUS_CONNECTED, (
        f"Expected dashboard storage status to show '{STORAGE_STATUS_CONNECTED}'."
    )

    dashboard_page.select_file_for_upload(str(SMALL_TEXT_FILE_PATH))

    assert dashboard_page.get_selected_upload_file_name() == SMALL_TEXT_FILE_NAME, (
        f"Expected selected upload file name to be '{SMALL_TEXT_FILE_NAME}'."
    )

    dashboard_page.submit_upload()

    assert dashboard_page.get_flash_message_text() == UPLOAD_SUCCESS_MESSAGE, (
        f"Expected upload success message to be '{UPLOAD_SUCCESS_MESSAGE}'."
    )
    assert dashboard_page.has_files_table() is True, (
        "Expected the files table to be visible after a successful upload."
    )
    assert dashboard_page.contains_file_name(SMALL_TEXT_FILE_NAME) is True, (
        f"Expected uploaded file '{SMALL_TEXT_FILE_NAME}' to appear in the dashboard."
    )

    uploaded_file_metadata = dashboard_page.get_file_metadata_by_name(
        SMALL_TEXT_FILE_NAME
    )

    assert uploaded_file_metadata["filename"] == SMALL_TEXT_FILE_NAME, (
        f"Expected uploaded row filename to be '{SMALL_TEXT_FILE_NAME}'."
    )
    assert uploaded_file_metadata["uploaded_by"] == ADMIN_USERNAME, (
        f"Expected uploaded row 'uploaded by' to be '{ADMIN_USERNAME}'."
    )
    assert uploaded_file_metadata["content_type"] == "text/plain", (
        "Expected uploaded text file content type to be 'text/plain'."
    )
    assert uploaded_file_metadata["object_key"].startswith("portal-uploads/"), (
        "Expected uploaded object key to start with 'portal-uploads/'."
    )
    assert SMALL_TEXT_FILE_NAME in uploaded_file_metadata["object_key"], (
        f"Expected uploaded object key to contain '{SMALL_TEXT_FILE_NAME}'."
    )
    assert uploaded_file_metadata["uploaded_at"] != "N/A", (
        "Expected uploaded row to show a real upload timestamp."
    )
    assert uploaded_file_metadata["size"] != "", (
        "Expected uploaded row to show a non-empty file size."
    )

    backend_file_names = [stored_file.filename for stored_file in storage_service.list_files()]
    assert SMALL_TEXT_FILE_NAME in backend_file_names, (
        f"Expected backend storage to contain '{SMALL_TEXT_FILE_NAME}' after upload."
    )


@pytest.mark.smoke
def test_admin_can_upload_file_by_dragging_it(
    driver,
    base_url: str,
    reset_portal_state,
    storage_service,
) -> None:
    """
    Verify the admin user can upload a file by dragging it into the upload area.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.
        reset_portal_state: Fixture that resets portal runtime state for isolation.
        storage_service: Storage service fixture used for backend object verification.
    """
    _ = reset_portal_state
    dashboard_page = _sign_in_as_admin(driver, base_url)

    dashboard_page.drag_file_into_upload_input(str(PNG_FILE_PATH))

    assert dashboard_page.get_selected_upload_file_name() == PNG_FILE_NAME, (
        f"Expected dragged upload file name to be '{PNG_FILE_NAME}'."
    )

    dashboard_page.submit_upload()

    assert dashboard_page.get_flash_message_text() == UPLOAD_SUCCESS_MESSAGE, (
        f"Expected drag-and-drop upload success message to be '{UPLOAD_SUCCESS_MESSAGE}'."
    )
    assert dashboard_page.contains_file_name(PNG_FILE_NAME) is True, (
        f"Expected dragged file '{PNG_FILE_NAME}' to appear in the dashboard."
    )

    uploaded_file_metadata = dashboard_page.get_file_metadata_by_name(PNG_FILE_NAME)

    assert uploaded_file_metadata["content_type"] == "image/png", (
        "Expected uploaded image file content type to be 'image/png'."
    )

    backend_file_names = [stored_file.filename for stored_file in storage_service.list_files()]
    assert PNG_FILE_NAME in backend_file_names, (
        f"Expected backend storage to contain '{PNG_FILE_NAME}' after drag upload."
    )


@pytest.mark.smoke
def test_authenticated_user_can_download_existing_file(
    driver,
    base_url: str,
    download_directory: Path,
    reset_portal_state,
) -> None:
    """
    Verify an authenticated user can download an existing uploaded file.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.
        download_directory: Temporary browser download directory for the current test.
        reset_portal_state: Fixture that resets portal runtime state for isolation.
    """
    _ = reset_portal_state
    admin_dashboard_page = _sign_in_as_admin(driver, base_url)
    admin_dashboard_page.upload_file(str(SMALL_TEXT_FILE_PATH))

    assert (
        admin_dashboard_page.wait_for_flash_message_text(UPLOAD_SUCCESS_MESSAGE)
        == UPLOAD_SUCCESS_MESSAGE
    ), (
        f"Expected setup upload success message to be '{UPLOAD_SUCCESS_MESSAGE}'."
    )

    login_page = admin_dashboard_page.click_logout()

    assert login_page.is_loaded(), (
        "Expected logout to return the browser to the login page."
    )

    viewer_dashboard_page = _sign_in_as_viewer(driver, base_url)

    assert viewer_dashboard_page.contains_file_name(SMALL_TEXT_FILE_NAME) is True, (
        f"Expected viewer dashboard to show '{SMALL_TEXT_FILE_NAME}' before download."
    )

    viewer_dashboard_page.click_download_file_by_name(SMALL_TEXT_FILE_NAME)
    downloaded_file = _wait_for_download(download_directory, SMALL_TEXT_FILE_NAME)

    assert downloaded_file.exists() is True, (
        f"Expected downloaded file '{SMALL_TEXT_FILE_NAME}' to exist locally."
    )
    assert downloaded_file.read_bytes() == SMALL_TEXT_FILE_PATH.read_bytes(), (
        "Expected downloaded file bytes to match the originally uploaded file."
    )


@pytest.mark.smoke
def test_admin_can_delete_existing_file(
    driver,
    base_url: str,
    reset_portal_state,
    storage_service,
) -> None:
    """
    Verify the admin user can delete an existing uploaded file.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.
        reset_portal_state: Fixture that resets portal runtime state for isolation.
        storage_service: Storage service fixture used for backend object verification.
    """
    _ = reset_portal_state
    dashboard_page = _sign_in_as_admin(driver, base_url)
    dashboard_page.upload_file(str(SMALL_TEXT_FILE_PATH))

    assert (
        dashboard_page.wait_for_flash_message_text(UPLOAD_SUCCESS_MESSAGE)
        == UPLOAD_SUCCESS_MESSAGE
    ), (
        f"Expected setup upload success message to be '{UPLOAD_SUCCESS_MESSAGE}'."
    )
    assert dashboard_page.contains_file_name(SMALL_TEXT_FILE_NAME) is True, (
        f"Expected '{SMALL_TEXT_FILE_NAME}' to appear before delete."
    )

    dashboard_page.click_delete_file_by_name(SMALL_TEXT_FILE_NAME)

    assert (
        dashboard_page.wait_for_flash_message_text(DELETE_SUCCESS_MESSAGE)
        == DELETE_SUCCESS_MESSAGE
    ), (
        f"Expected delete success message to be '{DELETE_SUCCESS_MESSAGE}'."
    )
    assert dashboard_page.wait_until_file_name_not_visible(SMALL_TEXT_FILE_NAME) is True, (
        f"Expected '{SMALL_TEXT_FILE_NAME}' to no longer appear after delete."
    )
    assert dashboard_page.is_empty_state_visible() is True, (
        "Expected the empty-files state to be visible after deleting the only file."
    )

    backend_file_names = [stored_file.filename for stored_file in storage_service.list_files()]
    assert SMALL_TEXT_FILE_NAME not in backend_file_names, (
        f"Expected backend storage to no longer contain '{SMALL_TEXT_FILE_NAME}'."
    )
