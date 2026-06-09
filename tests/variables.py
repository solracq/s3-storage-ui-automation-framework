"""Shared test constants for Secure S3 File Portal UI automation."""

from pathlib import Path

TESTS_ROOT = Path(__file__).resolve().parent
TEST_DATA_DIR = TESTS_ROOT / "data"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
ADMIN_ROLE = "admin"

VIEWER_USERNAME = "viewer"
VIEWER_PASSWORD = "viewer123"
VIEWER_ROLE = "viewer"

STORAGE_STATUS_CONNECTED = "Connected"
HEALTH_STATUS_OK = "ok"
PORTAL_BUCKET_NAME = "secure-file-portal"

UPLOAD_SUCCESS_MESSAGE = "File uploaded successfully."
DELETE_SUCCESS_MESSAGE = "File deleted successfully."

SMALL_TEXT_FILE_NAME = "small_file.txt"
SMALL_TEXT_FILE_PATH = TEST_DATA_DIR / SMALL_TEXT_FILE_NAME

PNG_FILE_NAME = "colors.png"
PNG_FILE_PATH = TEST_DATA_DIR / PNG_FILE_NAME
