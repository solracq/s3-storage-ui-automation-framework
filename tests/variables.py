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
PORTAL_STORAGE_ENDPOINT = "minio:9000"
PORTAL_MODE_TEXT = "Phase 2 access-control build"
PORTAL_PAGE_HEADING = "Secure S3 File Portal"
PORTAL_PAGE_DESCRIPTION_SNIPPET = (
    "Phase 2 builds on the storage workflow foundation"
)
UPLOAD_LIMIT_NOTE_TEXT = "Maximum upload size: 1 MB per file."
EMPTY_FILES_MESSAGE = (
    "No files are stored yet. Upload a sample object to verify the MinIO "
    "integration end to end."
)
VIEWER_ROLE_STATUS_TEXT = "Download-Only Access"
INVALID_LOGIN_MESSAGE = "Invalid username or password."
EMPTY_UPLOAD_MESSAGE = "Please choose a file before uploading."
EMPTY_FILE_UPLOAD_MESSAGE = "Please upload a non-empty file."
OVERSIZE_UPLOAD_MESSAGE = (
    "Maximum upload size exceeded. This portal currently supports files up to 1 MB."
)
INVALID_USERNAME = "invalid-user"
INVALID_PASSWORD = "wrong-password"

UPLOAD_SUCCESS_MESSAGE = "File uploaded successfully."
DELETE_SUCCESS_MESSAGE = "File deleted successfully."

SMALL_TEXT_FILE_NAME = "small_file.txt"
SMALL_TEXT_FILE_PATH = TEST_DATA_DIR / SMALL_TEXT_FILE_NAME

PNG_FILE_NAME = "colors.png"
PNG_FILE_PATH = TEST_DATA_DIR / PNG_FILE_NAME

LARGE_FILE_WITHIN_LIMIT_NAME = "large-file.txt"
LARGE_FILE_WITHIN_LIMIT_PATH = TEST_DATA_DIR / LARGE_FILE_WITHIN_LIMIT_NAME

LARGE_FILE_EXCEEDS_LIMIT_NAME = "large-file-size-exeeded.txt"
LARGE_FILE_EXCEEDS_LIMIT_PATH = TEST_DATA_DIR / LARGE_FILE_EXCEEDS_LIMIT_NAME

TEXT_PLAIN_CONTENT_TYPE = "text/plain"
PNG_CONTENT_TYPE = "image/png"
