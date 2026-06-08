"""
Login page object for the Secure S3 File Portal.
"""

from __future__ import annotations

from selenium.webdriver.common.by import By

from tests.pages.dashboard.dashboard_page import DashboardPage
from tests.pages.base_page import BasePage

Locator = tuple[str, str]


class LoginPage(BasePage):
    """
    Represent the portal login page and its main interactions.
    """

    URL_PATH = "/login"

    # Stable data-testid selectors keep the page object independent from CSS styling changes.
    PAGE_ROOT: Locator = (By.CSS_SELECTOR, "[data-testid='login-page']")
    PAGE_HEADING: Locator = (By.CSS_SELECTOR, "[data-testid='login-heading']")
    PAGE_DESCRIPTION: Locator = (By.CSS_SELECTOR, "[data-testid='login-description']")
    LOGIN_NAV_LINK: Locator = (By.CSS_SELECTOR, "[data-testid='login-nav-link']")
    LOGIN_FORM: Locator = (By.CSS_SELECTOR, "[data-testid='login-form']")
    USERNAME_INPUT: Locator = (By.CSS_SELECTOR, "[data-testid='username-input']")
    PASSWORD_INPUT: Locator = (By.CSS_SELECTOR, "[data-testid='password-input']")
    SUBMIT_BUTTON: Locator = (By.CSS_SELECTOR, "[data-testid='login-submit-button']")
    FLASH_MESSAGE: Locator = (By.CSS_SELECTOR, "[data-testid='login-flash-message']")
    DEMO_CREDENTIALS: Locator = (By.CSS_SELECTOR, "[data-testid='demo-credentials']")

    def login_as(self, username: str, password: str) -> None:
        """
        Sign in through the login form using the provided credentials.
        Args:
            username {str}: user's username
            password {str}: user's password
        """
        username_input = self.driver.find_element(*self.USERNAME_INPUT)
        password_input = self.driver.find_element(*self.PASSWORD_INPUT)

        username_input.clear()
        username_input.send_keys(username)

        password_input.clear()
        password_input.send_keys(password)

        self.driver.find_element(*self.SUBMIT_BUTTON).click()

    def login_as_expected_success(self, username: str, password: str) -> DashboardPage:
        """
        Sign in through the login form and return the dashboard page object.
        Args:
            username {str}: user's username
            password {str}: user's password
        Returns:
            DashboardPage: upon successful login, retrun of the dashoboard page.
        """
        self.login_as(username, password)
        return DashboardPage(self.driver)

    def click_login_nav_link(self) -> None:
        """
        Click the top-right Login navigation link.
        """
        self.driver.find_element(*self.LOGIN_NAV_LINK).click()

    def submit_login(self) -> None:
        """
        Click the sign-in button without filling the login fields first.
        """
        self.driver.find_element(*self.SUBMIT_BUTTON).click()

    def get_flash_message_text(self) -> str:
        """
        Return the visible login flash message text.
        """
        return self.driver.find_element(*self.FLASH_MESSAGE).text.strip()

    def is_loaded(self) -> bool:
        """
        Return whether the main login page elements are present and visible.
        """
        page_roots = self.driver.find_elements(*self.PAGE_ROOT)
        headings = self.driver.find_elements(*self.PAGE_HEADING)

        if not page_roots or not headings:
            return False

        return page_roots[0].is_displayed() and headings[0].is_displayed()
