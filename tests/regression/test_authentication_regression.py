"""
Regression coverage for portal authentication scenarios from the exploratory testing document.
"""

from __future__ import annotations

import pytest

from tests.pages.dashboard.dashboard_page import DashboardPage
from tests.pages.login.login_page import LoginPage
from tests.variables import (
    ADMIN_PASSWORD,
    ADMIN_USERNAME,
    LOGGED_OUT_SUCCESS_MESSAGE,
    PLEASE_SIGN_IN_MESSAGE,
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


@pytest.mark.regression
@pytest.mark.authentication
def test_valid_credentials_work_when_typed_and_pasted(driver, base_url: str, reset_portal_state) -> None:
    """
    Scenario 26 (from exploratory testing doc): Verify that valid credentials work when typed and when copy-pasted.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.
        reset_portal_state: Fixture that resets portal runtime state for isolation.
    """
    _ = reset_portal_state
    driver.get(base_url)
    login_page = LoginPage(driver)

    assert login_page.is_loaded(), (
        "Expected the login page to be displayed before validating credential input methods."
    )

    dashboard_page = login_page.login_as_expected_success(
        ADMIN_USERNAME,
        ADMIN_PASSWORD,
    )

    assert dashboard_page.is_loaded(), (
        "Expected the portal to accept credentials entered by typing."
    )

    login_page = dashboard_page.click_logout()

    assert login_page.is_loaded(), (
        "Expected logout after the typing path to return the user to the login page."
    )
    assert login_page.wait_for_flash_message_text(LOGGED_OUT_SUCCESS_MESSAGE) == LOGGED_OUT_SUCCESS_MESSAGE, (
        f"Expected logout message to be '{LOGGED_OUT_SUCCESS_MESSAGE}'."
    )

    login_page.paste_credentials(ADMIN_USERNAME, ADMIN_PASSWORD)
    dashboard_page = login_page.submit_login_expected_success()

    assert dashboard_page.is_loaded(), (
        "Expected the portal to accept credentials entered through the paste-style path."
    )


@pytest.mark.regression
@pytest.mark.authentication
def test_browser_autofill_login_is_accepted_when_available(driver, base_url: str, reset_portal_state) -> None:
    """
    Scenario 26 (from exploratory testing doc): Verify that browser autofill can be used when it is available.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.
        reset_portal_state: Fixture that resets portal runtime state for isolation.
    """
    _ = reset_portal_state
    driver.get(f"{base_url}/login")
    login_page = LoginPage(driver)

    assert login_page.is_loaded(), (
        "Expected the login page to be displayed before checking browser autofill behavior."
    )

    if not login_page.has_prefilled_credentials():
        pytest.skip(
            "Browser autofill is not available in the current automated environment."
        )

    dashboard_page = login_page.submit_login_expected_success()

    assert dashboard_page.is_loaded(), (
        "Expected the portal to accept credentials supplied by browser autofill."
    )


@pytest.mark.regression
@pytest.mark.authentication
def test_unauthenticated_access_to_protected_routes_redirects_to_login(driver, base_url: str, reset_portal_state) -> None:
    """
    Scenario 29 (from exploratory testing doc): Verify that protected portal routes redirect unauthenticated users to login.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.
        reset_portal_state: Fixture that resets portal runtime state for isolation.
    """
    _ = reset_portal_state

    driver.get(base_url)
    login_page = LoginPage(driver)

    assert login_page.is_loaded(), (
        "Expected unauthenticated access to the portal root URL to redirect to the login page."
    )
    assert login_page.wait_for_flash_message_text(PLEASE_SIGN_IN_MESSAGE) == PLEASE_SIGN_IN_MESSAGE, (
        f"Expected blocked root access message to be '{PLEASE_SIGN_IN_MESSAGE}'."
    )

    driver.get(f"{base_url}/audit-logs")
    login_page = LoginPage(driver)

    assert login_page.is_loaded(), (
        "Expected unauthenticated access to the audit log route to redirect to the login page."
    )
    assert login_page.wait_for_flash_message_text(PLEASE_SIGN_IN_MESSAGE) == PLEASE_SIGN_IN_MESSAGE, (
        f"Expected blocked audit log access message to be '{PLEASE_SIGN_IN_MESSAGE}'."
    )


@pytest.mark.regression
@pytest.mark.authentication
def test_logout_invalidates_the_portal_session(driver, base_url: str, reset_portal_state) -> None:
    """
    Scenario 30 (from exploratory testing doc): Verify that logout invalidates the session and blocks return to protected pages.

    Args:
        driver: Selenium WebDriver fixture used to automate the browser.
        base_url: Base portal URL used to open the application under test.
        reset_portal_state: Fixture that resets portal runtime state for isolation.
    """
    _ = reset_portal_state
    dashboard_page = _sign_in_as_admin(driver, base_url)
    login_page = dashboard_page.click_logout()

    assert login_page.is_loaded(), (
        "Expected logout to return the user to the login page."
    )
    assert login_page.wait_for_flash_message_text(LOGGED_OUT_SUCCESS_MESSAGE) == LOGGED_OUT_SUCCESS_MESSAGE, f"Expected logout message to be '{LOGGED_OUT_SUCCESS_MESSAGE}'."

    driver.back()
    driver.refresh()
    login_page = LoginPage(driver)

    assert login_page.is_loaded(timeout_seconds=10), (
        "Expected browser back navigation plus refresh after logout to return the user to the login page."
    )

    driver.get(base_url)
    login_page = LoginPage(driver)

    assert login_page.is_loaded(), (
        "Expected direct dashboard access after logout to redirect back to the login page."
    )
    assert login_page.wait_for_flash_message_text(PLEASE_SIGN_IN_MESSAGE) == PLEASE_SIGN_IN_MESSAGE, (
        f"Expected blocked post-logout access message to be '{PLEASE_SIGN_IN_MESSAGE}'."
    )
