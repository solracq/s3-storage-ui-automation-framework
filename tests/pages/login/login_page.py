"""
Login page object for the Secure S3 File Portal.
"""

from __future__ import annotations

from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

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

    # ### Action Methods ###

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
            DashboardPage: upon successful login, return the dashboard page.
        """
        self.login_as(username, password)
        return DashboardPage(self.driver)

    def login_as_expected_failure(self, username: str, password: str) -> "LoginPage":
        """
        Submit invalid credentials and remain on the login page.
        Args:
            username {str}: user's username
            password {str}: user's password
        Returns:
            LoginPage: upon unsuccessful    login, return the same login page.
        """
        self.login_as(username, password)
        return self

    def click_login_nav_link(self) -> None:
        """
        Click the top-right Login navigation link.
        """
        self.driver.find_element(*self.LOGIN_NAV_LINK).click()

    def paste_credentials(self, username: str, password: str) -> None:
        """
        Populate the login fields through a paste-style browser event path.

        Args:
            username {str}: user's username
            password {str}: user's password
        """
        username_input = self.driver.find_element(*self.USERNAME_INPUT)
        password_input = self.driver.find_element(*self.PASSWORD_INPUT)

        self.driver.execute_script(
            """
            const [usernameInput, passwordInput, usernameValue, passwordValue] = arguments;

            for (const [element, value] of [
                [usernameInput, usernameValue],
                [passwordInput, passwordValue],
            ]) {
                element.focus();
                element.value = "";

                const clipboardData = new DataTransfer();
                clipboardData.setData("text/plain", value);

                element.dispatchEvent(
                    new ClipboardEvent("paste", {
                        clipboardData,
                        bubbles: true,
                        cancelable: true,
                    }),
                );

                element.value = value;
                element.dispatchEvent(new Event("input", { bubbles: true }));
                element.dispatchEvent(new Event("change", { bubbles: true }));
            }
            """,
            username_input,
            password_input,
            username,
            password,
        )

    def submit_login_expected_success(self) -> DashboardPage:
        """
        Submit the login form and return the dashboard page object.

        Returns:
            DashboardPage: dashboard page object after a successful login submission.
        """
        self.submit_login()
        return DashboardPage(self.driver)

    def submit_login(self) -> None:
        """
        Click the sign-in button without filling the login fields first.
        """
        self.driver.find_element(*self.SUBMIT_BUTTON).click()

    # ### Helper Methods ###

    def clear_form(self) -> None:
        """
        Helper: clear the username and password fields.
        """
        self.driver.find_element(*self.USERNAME_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).clear()

    def get_flash_message_text(self) -> str:
        """
        Helper: return the visible login flash message text.
        """
        return self.driver.find_element(*self.FLASH_MESSAGE).text.strip()

    def get_username_value(self) -> str:
        """
        Helper: return the current username field value.
        """
        return self.driver.find_element(*self.USERNAME_INPUT).get_attribute("value").strip()

    def get_password_value(self) -> str:
        """
        Helper: return the current password field value.
        """
        return self.driver.find_element(*self.PASSWORD_INPUT).get_attribute("value").strip()

    def has_prefilled_credentials(self) -> bool:
        """
        Helper: return whether the login fields already contain credential values.
        """
        return bool(self.get_username_value()) and bool(self.get_password_value())

    def wait_for_flash_message_text(self, expected_text: str, timeout_seconds: int = 10) -> str:
        """
        Helper: wait until the login flash message matches the expected text.
        """
        WebDriverWait(self.driver, timeout_seconds).until(
            lambda driver: driver.find_elements(*self.FLASH_MESSAGE)
            and driver.find_element(*self.FLASH_MESSAGE).text.strip() == expected_text
        )
        return self.get_flash_message_text()

    def is_loaded(self, timeout_seconds: int = 5) -> bool:
        """
        Helper: return whether the main login page elements are present and visible.
        """
        def _login_page_is_ready(driver) -> bool:
            try:
                page_roots = driver.find_elements(*self.PAGE_ROOT)
                headings = driver.find_elements(*self.PAGE_HEADING)

                if not page_roots or not headings:
                    return False

                return "/login" in driver.current_url
            except WebDriverException:
                return False

        try:
            return bool(WebDriverWait(self.driver, timeout_seconds).until(_login_page_is_ready))
        except TimeoutException:
            return False
