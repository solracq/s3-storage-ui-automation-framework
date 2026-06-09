"""
Shared pytest fixtures for Secure S3 File Portal UI automation.
"""

from __future__ import annotations

import os
from collections.abc import Generator
from pathlib import Path

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
def download_directory(tmp_path: Path) -> Path:
    """
    Return the per-test browser download directory.
    """
    return tmp_path


def _reset_portal_runtime_state() -> None:
    """
    Reset stored files, audit entries, and demo users for repeatable smoke runs.
    """
    from app.storage_portal.services.audit import AuditService
    from app.storage_portal.services.auth import AuthService
    from app.storage_portal.services.storage import StorageService
    from app.storage_portal.settings import get_settings

    settings = get_settings()
    storage_service = StorageService(settings)
    auth_service = AuthService(settings)
    audit_service = AuditService(settings)

    storage_service.delete_all_files()
    audit_service.clear_entries()
    auth_service.seed_default_users(overwrite=True)


@pytest.fixture
def reset_portal_state() -> Generator[None, None, None]:
    """
    Reset the portal state before and after each smoke test that mutates data.
    """
    _reset_portal_runtime_state()
    yield
    _reset_portal_runtime_state()


@pytest.fixture
def storage_service():
    """
    Return a storage service instance for backend verification in UI smoke tests.
    """
    from app.storage_portal.services.storage import StorageService
    from app.storage_portal.settings import get_settings

    return StorageService(get_settings())


@pytest.fixture
def driver(
    browser_name: str,
    download_directory: Path,
) -> Generator[webdriver.Chrome, None, None]:
    """
    Create and dispose the WebDriver instance used by UI smoke tests.
    """
    if browser_name != "chrome":
        raise ValueError(
            "Initial smoke coverage currently supports PORTAL_BROWSER=chrome only."
        )

    options = webdriver.ChromeOptions()
    options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": str(download_directory.resolve()),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        },
    )

    if _parse_bool_env(os.getenv("PORTAL_HEADLESS"), default=True):
        options.add_argument("--headless=new")

    options.add_argument("--window-size=1440,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    chrome_driver = webdriver.Chrome(options=options)
    chrome_driver.implicitly_wait(int(os.getenv("PORTAL_IMPLICIT_WAIT_SECONDS", "5")))
    chrome_driver.execute_cdp_cmd(
        "Page.setDownloadBehavior",
        {
            "behavior": "allow",
            "downloadPath": str(download_directory.resolve()),
        },
    )

    yield chrome_driver

    chrome_driver.quit()
