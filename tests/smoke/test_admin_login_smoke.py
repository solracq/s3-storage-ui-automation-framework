"""
Smoke tests for critical Secure S3 File Portal login coverage.
"""

from __future__ import annotations

import pytest

from tests.pages.login.login_page import LoginPage


@pytest.mark.smoke
def test_admin_can_sign_in_and_reach_dashboard(driver, base_url: str) -> None:
    """
    Verify the admin demo user can sign in and reach the dashboard.
    """
    driver.get(base_url)

    login_page = LoginPage(driver)

    assert login_page.is_loaded(), (
        "Expected unauthenticated root access to redirect to the login page."
    )

    dashboard_page = login_page.login_as_expected_success("admin", "admin123")

    assert dashboard_page.is_loaded(), (
        "Expected successful admin login to land on the dashboard."
    )
    assert dashboard_page.get_current_user_text() == "admin"
    assert dashboard_page.get_current_role_text() == "admin"
    assert dashboard_page.get_storage_status_text() == "Connected"
    assert dashboard_page.is_upload_panel_visible() is True
