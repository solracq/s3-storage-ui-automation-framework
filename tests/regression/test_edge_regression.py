"""
Regression coverage for portal edge scenarios from the exploratory testing document.
"""

from __future__ import annotations

import pytest

from tests.pages.dashboard.dashboard_page import DashboardPage
from tests.pages.login.login_page import LoginPage
from tests.variables import (
    ADMIN_PASSWORD,
    ADMIN_USERNAME,
    EDGE_FILE_TYPE_UPLOAD_CASES,
    LONG_UNUSUAL_FILE_NAME,
    LONG_UNUSUAL_FILE_PATH,
    UPLOAD_SUCCESS_MESSAGE,
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


def _upload_file_and_wait(
    dashboard_page: DashboardPage,
    file_path: str,
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
    dashboard_page.upload_file(file_path)

    assert (
        dashboard_page.wait_for_flash_message_text(UPLOAD_SUCCESS_MESSAGE)
        == UPLOAD_SUCCESS_MESSAGE
    ), f"Expected upload success message to be '{UPLOAD_SUCCESS_MESSAGE}'."
    assert dashboard_page.wait_until_file_name_visible(expected_filename) is True, (
        f"Expected '{expected_filename}' to appear in the Stored Files section."
    )

    return dashboard_page.get_file_metadata_by_name(expected_filename)


@pytest.mark.regression
@pytest.mark.edge
def test_unusual_or_long_file_name_uploads_successfully(
    driver,
    base_url: str,
    reset_portal_state,
    storage_service,
) -> None:
    """
    Scenario 21 (from exploratory testing doc): Verify that a file with an unusual or long name uploads successfully.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.
        reset_portal_state: Fixture that resets portal runtime state for isolation.
        storage_service: Storage service fixture used for backend object verification.
    """
    _ = reset_portal_state
    dashboard_page = _sign_in_as_admin(driver, base_url)
    uploaded_file_metadata = _upload_file_and_wait(
        dashboard_page,
        str(LONG_UNUSUAL_FILE_PATH),
        LONG_UNUSUAL_FILE_NAME,
    )

    assert uploaded_file_metadata["filename"] == LONG_UNUSUAL_FILE_NAME, (
        f"Expected visible file name to be '{LONG_UNUSUAL_FILE_NAME}'."
    )
    assert uploaded_file_metadata["object_key"].startswith("portal-uploads/"), (
        "Expected uploaded object key to start with the portal upload folder prefix."
    )
    assert uploaded_file_metadata["object_key"].endswith(LONG_UNUSUAL_FILE_NAME), (
        "Expected uploaded object key to preserve the unusual or long file name."
    )

    backend_file_names = [stored_file.filename for stored_file in storage_service.list_files()]
    assert LONG_UNUSUAL_FILE_NAME in backend_file_names, (
        f"Expected backend storage to contain '{LONG_UNUSUAL_FILE_NAME}'."
    )


@pytest.mark.regression
@pytest.mark.edge
def test_multiple_supported_file_types_upload_successfully(
    driver,
    base_url: str,
    reset_portal_state,
    storage_service,
) -> None:
    """
    Scenario 23 (from exploratory testing doc): Verify that multiple supported file types can be uploaded successfully.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.
        reset_portal_state: Fixture that resets portal runtime state for isolation.
        storage_service: Storage service fixture used for backend object verification.
    """
    _ = reset_portal_state
    dashboard_page = _sign_in_as_admin(driver, base_url)

    for expected_filename, file_path in EDGE_FILE_TYPE_UPLOAD_CASES:
        uploaded_file_metadata = _upload_file_and_wait(
            dashboard_page,
            str(file_path),
            expected_filename,
        )

        assert uploaded_file_metadata["filename"] == expected_filename, (
            f"Expected visible file name to be '{expected_filename}'."
        )
        assert uploaded_file_metadata["object_key"].endswith(expected_filename), (
            f"Expected object key to preserve '{expected_filename}'."
        )

    backend_file_names = {stored_file.filename for stored_file in storage_service.list_files()}
    expected_file_names = {file_name for file_name, _file_path in EDGE_FILE_TYPE_UPLOAD_CASES}

    assert dashboard_page.get_file_row_count() == len(EDGE_FILE_TYPE_UPLOAD_CASES), (
        "Expected one dashboard row per uploaded edge-case file type."
    )
    assert expected_file_names.issubset(backend_file_names), (
        "Expected backend storage to contain every uploaded edge-case file type."
    )
