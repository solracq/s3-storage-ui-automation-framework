"""Shared pytest fixtures for Secure S3 File Portal UI automation."""

from __future__ import annotations

import os
from collections.abc import Generator

import pytest
from selenium import webdriver


def _parse_bool_env(raw_value: str | None, *, default: bool) -> bool:
    """
    Convert a simple environment-variable string into a boolean flag.
    """
    if raw_value is None:
        return default

    normalized_value = raw_value.strip().lower()

    if normalized_value in {"1", "true", "yes", "on"}:
        return True

    if normalized_value in {"0", "false", "no", "off"}:
        return False

    return default


@pytest.fixture(scope="session")
def base_url() -> str:
    """
    Return the portal base URL used by local UI automation runs.
    """
    return os.getenv("PORTAL_BASE_URL", "http://localhost:8000").rstrip("/")


@pytest.fixture(scope="session")
def browser_name() -> str:
    """
    Return the requested browser name for the current pytest session.
    """
    return os.getenv("PORTAL_BROWSER", "chrome").strip().lower()


@pytest.fixture
def driver(browser_name: str) -> Generator[webdriver.Chrome, None, None]:
    """
    Create and dispose the WebDriver instance used by UI smoke tests.
    """
    if browser_name != "chrome":
        raise ValueError(
            "Initial smoke coverage currently supports PORTAL_BROWSER=chrome only."
        )

    options = webdriver.ChromeOptions()

    if _parse_bool_env(os.getenv("PORTAL_HEADLESS"), default=True):
        options.add_argument("--headless=new")

    options.add_argument("--window-size=1440,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    chrome_driver = webdriver.Chrome(options=options)
    chrome_driver.implicitly_wait(int(os.getenv("PORTAL_IMPLICIT_WAIT_SECONDS", "5")))

    yield chrome_driver

    chrome_driver.quit()
