"""
Login page object for the Secure S3 File Portal.
"""

from __future__ import annotations

from selenium.webdriver.common.by import By

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
    LOGIN_FORM: Locator = (By.CSS_SELECTOR, "[data-testid='login-form']")
    USERNAME_INPUT: Locator = (By.CSS_SELECTOR, "[data-testid='username-input']")
    PASSWORD_INPUT: Locator = (By.CSS_SELECTOR, "[data-testid='password-input']")
    SUBMIT_BUTTON: Locator = (By.CSS_SELECTOR, "[data-testid='login-submit-button']")
    FLASH_MESSAGE: Locator = (By.CSS_SELECTOR, "[data-testid='login-flash-message']")
    DEMO_CREDENTIALS: Locator = (By.CSS_SELECTOR, "[data-testid='demo-credentials']")

    def login_as(self, username: str, password: str) -> None:
        """
        Sign in through the login form using the provided credentials.
        """
        username_input = self.driver.find_element(*self.USERNAME_INPUT)
        password_input = self.driver.find_element(*self.PASSWORD_INPUT)

        username_input.clear()
        username_input.send_keys(username)

        password_input.clear()
        password_input.send_keys(password)

        self.driver.find_element(*self.SUBMIT_BUTTON).click()
