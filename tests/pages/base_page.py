"""Shared base page abstraction for Page Object Model classes."""


class BasePage:
    """Provide the common structure shared by portal page objects."""

    URL_PATH = "/"

    def __init__(self, driver) -> None:
        """Store the WebDriver instance used by the page object."""
        self.driver = driver
