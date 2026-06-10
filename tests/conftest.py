"""
Shared pytest fixtures for Secure S3 File Portal UI automation.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
from collections.abc import Generator
from pathlib import Path
from urllib.request import urlopen

import pytest
from selenium import webdriver

PROJECT_ROOT = Path(__file__).resolve().parent.parent


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


def _resolve_chrome_binary() -> str | None:
    """
    Resolve the Chrome/Chromium binary path for local and Jenkins-driven runs.
    """
    candidate_values = [
        os.getenv("PORTAL_CHROME_BINARY"),
        os.getenv("CHROME_BIN"),
        "google-chrome",
        "google-chrome-stable",
        "chromium-browser",
        "chromium",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ]

    for candidate in candidate_values:
        if not candidate:
            continue

        resolved_command = shutil.which(candidate)
        if resolved_command:
            return resolved_command

        candidate_path = Path(candidate)
        if candidate_path.is_file():
            return str(candidate_path)

    return None


class MinioServiceController:
    """
    Stop and restore the local MinIO Compose service for outage-based UI tests.
    """

    def __init__(self, project_root: Path, base_url: str) -> None:
        self._project_root = project_root
        self._base_url = base_url
        self._service_stopped = False

    def stop(self) -> dict[str, object]:
        """
        Stop the MinIO service and wait until the portal health endpoint degrades.
        """
        self._run_compose_command("stop", "minio")
        self._service_stopped = True
        return self.wait_for_storage_ready(expected=False, timeout_seconds=60)

    def start(self) -> dict[str, object]:
        """
        Start the MinIO service and wait until the portal health endpoint recovers.
        """
        self._run_compose_command("start", "minio")
        payload = self.wait_for_storage_ready(expected=True, timeout_seconds=60)
        self._service_stopped = False
        return payload

    def ensure_started(self) -> None:
        """
        Restore MinIO if the current test stopped it.
        """
        if self._service_stopped:
            self.start()

    def read_health_payload(self) -> dict[str, object]:
        """
        Read and decode the current `/health` payload from the running portal.
        """
        with urlopen(f"{self._base_url}/health", timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))

    def wait_for_storage_ready(
        self,
        *,
        expected: bool,
        timeout_seconds: int = 30,
    ) -> dict[str, object]:
        """
        Poll the portal health endpoint until storage readiness reaches the expected state.
        """
        deadline = time.monotonic() + timeout_seconds
        last_payload: dict[str, object] | None = None
        last_error: Exception | None = None

        while time.monotonic() < deadline:
            try:
                payload = self.read_health_payload()
                last_payload = payload
                if payload.get("storage_ready") is expected:
                    return payload
            except Exception as exc:
                last_error = exc

            time.sleep(1)

        expected_state = "ready" if expected else "unavailable"
        extra_context = (
            f" Last health payload: {last_payload!r}."
            if last_payload is not None
            else f" Last error: {last_error!r}."
        )
        raise AssertionError(
            f"Timed out waiting for MinIO storage to become {expected_state}."
            f"{extra_context}"
        )

    def _run_compose_command(self, *args: str) -> None:
        """
        Run one Docker Compose command against the local project.
        """
        try:
            subprocess.run(
                ["docker", "compose", *args],
                cwd=self._project_root,
                check=True,
                capture_output=True,
                text=True,
            )
        except FileNotFoundError as exc:
            raise AssertionError(
                "Docker is required for the MinIO outage tests, but the `docker` "
                "command was not found."
            ) from exc
        except subprocess.CalledProcessError as exc:
            stderr = (exc.stderr or "").strip()
            stdout = (exc.stdout or "").strip()
            details = stderr or stdout or str(exc)
            raise AssertionError(
                f"Docker Compose command `docker compose {' '.join(args)}` failed: {details}"
            ) from exc


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
def minio_service_controller(base_url: str) -> Generator[MinioServiceController, None, None]:
    """
    Provide a helper that can stop and restore MinIO around outage-oriented UI tests.
    """
    controller = MinioServiceController(PROJECT_ROOT, base_url)
    yield controller
    controller.ensure_started()


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
    chrome_binary = _resolve_chrome_binary()
    if chrome_binary:
        options.binary_location = chrome_binary

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
