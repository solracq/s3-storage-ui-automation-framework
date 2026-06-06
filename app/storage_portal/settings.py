"""
Application configuration for the Secure S3 File Portal.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_DIR = PROJECT_ROOT / "runtime"
MEBIBYTE = 1024 * 1024
MULTIPART_GRACE_BYTES = 4 * 1024


def _parse_bool(value: str, default: bool = False) -> bool:
    """
    Convert an environment variable string into a boolean.
    """
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    return default


def _parse_int(value: str, default: int) -> int:
    """
    Convert an environment variable string into an integer.
    """
    try:
        return int(value.strip())
    except (TypeError, ValueError):
        return default


def _path_from_env(name: str, default: Path) -> Path:
    """
    Read a path from the environment and normalize it to an absolute path.
    """
    value = os.getenv(name)
    if not value:
        return default

    candidate = Path(value)
    if candidate.is_absolute():
        return candidate

    return PROJECT_ROOT / candidate


@dataclass(frozen=True)
class Settings:
    """
    Settings used by the portal application and local scripts.
    """

    app_name: str
    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket_name: str
    minio_secure: bool
    default_upload_actor: str
    max_upload_size_bytes: int
    session_secret_key: str
    demo_users_file: Path
    audit_log_file: Path

    @property
    def max_upload_size_label(self) -> str:
        """
        Return the configured upload limit in a UI-friendly format.
        """
        if self.max_upload_size_bytes % MEBIBYTE == 0:
            return f"{self.max_upload_size_bytes // MEBIBYTE} MB"
        return f"{self.max_upload_size_bytes} bytes"

    @property
    def max_upload_request_size_bytes(self) -> int:
        """
        Return the allowed multipart request size including small form overhead.
        """
        return self.max_upload_size_bytes + MULTIPART_GRACE_BYTES


@lru_cache
def get_settings() -> Settings:
    """
    Build and cache the application settings object.
    """
    return Settings(
        app_name=os.getenv("APP_NAME", "Secure S3 File Portal"),
        minio_endpoint=os.getenv("MINIO_ENDPOINT", "localhost:9000"),
        minio_access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
        minio_secret_key=os.getenv("MINIO_SECRET_KEY", "minioadmin123"),
        minio_bucket_name=os.getenv("MINIO_BUCKET_NAME", "secure-file-portal"),
        minio_secure=_parse_bool(os.getenv("MINIO_SECURE", "false")),
        default_upload_actor=os.getenv("DEFAULT_UPLOAD_ACTOR", "phase1-demo-admin"),
        max_upload_size_bytes=_parse_int(
            os.getenv("MAX_UPLOAD_SIZE_BYTES", "1048576"),
            default=1048576,
        ),
        session_secret_key=os.getenv("SESSION_SECRET_KEY", "local-phase2-demo-secret"),
        demo_users_file=_path_from_env(
            "DEMO_USERS_FILE",
            RUNTIME_DIR / "demo-users.json",
        ),
        audit_log_file=_path_from_env(
            "AUDIT_LOG_FILE",
            RUNTIME_DIR / "audit-log.json",
        ),
    )
