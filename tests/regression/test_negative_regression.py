"""
Regression coverage for portal negative scenarios from the exploratory testing document.
"""

from __future__ import annotations

import pytest

from tests.pages.dashboard.dashboard_page import DashboardPage
from tests.pages.login.login_page import LoginPage
from tests.variables import (
    ADMIN_PASSWORD,
    ADMIN_USERNAME,
    EMPTY_FILE_PATH,
    EMPTY_FILE_UPLOAD_MESSAGE,
    HEALTH_STATUS_DEGRADED,
    NON_ASCII_FILE_NAME,
    NON_ASCII_FILE_PATH,
    NON_ASCII_UPLOAD_MESSAGE,
    STORAGE_STATUS_UNAVAILABLE,
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


@pytest.mark.regression
@pytest.mark.negative
def test_empty_file_upload_is_rejected(driver, base_url: str, reset_portal_state, storage_service) -> None:
    """
    Scenario 17 (from exploratory testing doc): Verify that an empty file cannot be uploaded.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.
        reset_portal_state: Fixture that resets portal runtime state for isolation.
        storage_service: Storage service fixture used for backend object verification.
    """
    _ = reset_portal_state
    dashboard_page = _sign_in_as_admin(driver, base_url)

    dashboard_page.upload_file(str(EMPTY_FILE_PATH))

    assert  dashboard_page.wait_for_flash_message_text(EMPTY_FILE_UPLOAD_MESSAGE) == EMPTY_FILE_UPLOAD_MESSAGE, (
        f"Expected empty-file upload message to be '{EMPTY_FILE_UPLOAD_MESSAGE}'."
    )
    assert dashboard_page.is_empty_state_visible() is True, (
        "Expected the empty-files state to remain visible after empty-file rejection."
    )
    assert dashboard_page.get_file_row_count() == 0, (
        "Expected no file rows to be displayed after the empty-file rejection."
    )
    assert storage_service.list_files() == [], (
        "Expected backend storage to remain empty after the empty-file rejection."
    )


@pytest.mark.regression
@pytest.mark.negative
def test_non_ascii_filename_upload_is_rejected(driver, base_url: str, reset_portal_state, storage_service) -> None:
    """
    Scenario 19 (from exploratory testing doc): Verify that a non-ASCII file name is rejected.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.
        reset_portal_state: Fixture that resets portal runtime state for isolation.
        storage_service: Storage service fixture used for backend object verification.
    """
    _ = reset_portal_state
    dashboard_page = _sign_in_as_admin(driver, base_url)

    dashboard_page.upload_file(str(NON_ASCII_FILE_PATH))
    flash_message_text = dashboard_page.wait_for_any_flash_message_text()

    assert flash_message_text == NON_ASCII_UPLOAD_MESSAGE, (
        f"Expected non-ASCII upload message to be '{NON_ASCII_UPLOAD_MESSAGE}'."
    )
    assert dashboard_page.contains_file_name(NON_ASCII_FILE_NAME) is False, (
        f"Expected '{NON_ASCII_FILE_NAME}' not to appear after rejected upload."
    )
    assert dashboard_page.get_file_row_count() == 0, (
        "Expected no file rows to be displayed after the non-ASCII upload rejection."
    )
    assert storage_service.list_files() == [], (
        "Expected backend storage to remain empty after the non-ASCII upload rejection."
    )


@pytest.mark.regression
@pytest.mark.negative
def test_portal_stays_accessible_when_minio_is_unavailable(driver, base_url: str, minio_service_controller) -> None:
    """
    Scenario 20 (from exploratory testing doc): Verify that the portal degrades gracefully when MinIO is unavailable.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.
        minio_service_controller: Fixture that can stop and restore MinIO for outage testing.
    """
    health_payload = minio_service_controller.stop()
    dashboard_page = _sign_in_as_viewer(driver, base_url)

    assert dashboard_page.is_loaded(), (
        "Expected the dashboard to remain accessible even while MinIO is unavailable."
    )
    assert dashboard_page.wait_for_storage_status_text(STORAGE_STATUS_UNAVAILABLE) == STORAGE_STATUS_UNAVAILABLE, (
        f"Expected storage status to show '{STORAGE_STATUS_UNAVAILABLE}' during the outage."
    )
    assert dashboard_page.is_storage_error_message_visible() is True, (
        "Expected a visible storage error message while MinIO is unavailable."
    )
    assert dashboard_page.get_storage_error_message_text() != "", (
        "Expected the dashboard to show a non-empty storage error message during the outage."
    )
    assert health_payload["status"] == HEALTH_STATUS_DEGRADED, (
        f"Expected health status to be '{HEALTH_STATUS_DEGRADED}' while MinIO is unavailable."
    )
    assert health_payload["storage_ready"] is False, (
        "Expected the health endpoint to report storage_ready as false during the outage."
    )
