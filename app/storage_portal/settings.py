"""
App's configuration layer.
It is the bridge between Compose env variables and the Python application. It reads env
variables once and turn them into a small Python object the rest of the app can use.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache


def _parse_bool(value: str, default: bool = False) -> bool:
    """
    Defined for MINIO_SECURE, as the MinIO client expects a real boolean, not a string.

    Args:
        value (str): input value
        default (bool, optional): Defaults to False.

    Returns:
        bool: retruns the pased bolean value
    """
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    return default


@dataclass(frozen=True)
class Settings:
    """
    Defining a settings class, where settings cannot be modified at runtime.
    """
    app_name: str
    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket_name: str
    minio_secure: bool
    default_upload_actor: str


@lru_cache
def get_settings() -> Settings:
    """
    Method to get settings. 
    @lru_cache makes get_settings run once and reuse the same settings object
    Returns:
        Settings: return settings object
    """
    return Settings(
        app_name=os.getenv("APP_NAME", "Secure S3 File Portal"),
        minio_endpoint=os.getenv("MINIO_ENDPOINT", "localhost:9000"),
        minio_access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
        minio_secret_key=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
        minio_bucket_name=os.getenv("MINIO_BUCKET_NAME", "secure-file-portal"),
        minio_secure=_parse_bool(os.getenv("MINIO_SECURE", "false")),
        default_upload_actor=os.getenv("DEFAULT_UPLOAD_ACTOR", "phase1-demo-admin"),
    )
