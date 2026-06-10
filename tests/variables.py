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
STORAGE_STATUS_UNAVAILABLE = "Unavailable"
HEALTH_STATUS_OK = "ok"
HEALTH_STATUS_DEGRADED = "degraded"
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
NON_ASCII_UPLOAD_MESSAGE = (
    "unsupported metadata value は.txt; only US-ASCII encoded characters are "
    "supported"
)
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

LONG_UNUSUAL_FILE_NAME = (
    "sdfaflaf;lfad;lkaf;lkfdajk;ljeroijfd98438943%$#YGREW%TS%#HJYJ%JJYTDD%^JJ%S%HTHS.txt"
)
LONG_UNUSUAL_FILE_PATH = TEST_DATA_DIR / LONG_UNUSUAL_FILE_NAME

EMPTY_FILE_NAME = "empty.txt"
EMPTY_FILE_PATH = TEST_DATA_DIR / EMPTY_FILE_NAME

NON_ASCII_FILE_NAME = "は.txt"
NON_ASCII_FILE_PATH = TEST_DATA_DIR / NON_ASCII_FILE_NAME

LARGE_FILE_WITHIN_LIMIT_NAME = "large-file.txt"
LARGE_FILE_WITHIN_LIMIT_PATH = TEST_DATA_DIR / LARGE_FILE_WITHIN_LIMIT_NAME

LARGE_FILE_EXCEEDS_LIMIT_NAME = "large-file-size-exeeded.txt"
LARGE_FILE_EXCEEDS_LIMIT_PATH = TEST_DATA_DIR / LARGE_FILE_EXCEEDS_LIMIT_NAME

PDF_FILE_NAME = "sample-document.pdf"
PDF_FILE_PATH = TEST_DATA_DIR / PDF_FILE_NAME

DOCX_FILE_NAME = "sample-report.docx"
DOCX_FILE_PATH = TEST_DATA_DIR / DOCX_FILE_NAME

CSV_FILE_NAME = "sample-data.csv"
CSV_FILE_PATH = TEST_DATA_DIR / CSV_FILE_NAME

JPEG_FILE_NAME = "sample-photo.jpeg"
JPEG_FILE_PATH = TEST_DATA_DIR / JPEG_FILE_NAME

MP4_FILE_NAME = "sample-video.mp4"
MP4_FILE_PATH = TEST_DATA_DIR / MP4_FILE_NAME

WAV_FILE_NAME = "sample-audio.wav"
WAV_FILE_PATH = TEST_DATA_DIR / WAV_FILE_NAME

MARKDOWN_FILE_NAME = "sample-notes.md"
MARKDOWN_FILE_PATH = TEST_DATA_DIR / MARKDOWN_FILE_NAME

NO_EXTENSION_FILE_NAME = "sample-no-extension"
NO_EXTENSION_FILE_PATH = TEST_DATA_DIR / NO_EXTENSION_FILE_NAME

EDGE_FILE_TYPE_UPLOAD_CASES = (
    (SMALL_TEXT_FILE_NAME, SMALL_TEXT_FILE_PATH),
    (PDF_FILE_NAME, PDF_FILE_PATH),
    (DOCX_FILE_NAME, DOCX_FILE_PATH),
    (CSV_FILE_NAME, CSV_FILE_PATH),
    (JPEG_FILE_NAME, JPEG_FILE_PATH),
    (PNG_FILE_NAME, PNG_FILE_PATH),
    (MP4_FILE_NAME, MP4_FILE_PATH),
    (WAV_FILE_NAME, WAV_FILE_PATH),
    (MARKDOWN_FILE_NAME, MARKDOWN_FILE_PATH),
    (NO_EXTENSION_FILE_NAME, NO_EXTENSION_FILE_PATH),
)

TEXT_PLAIN_CONTENT_TYPE = "text/plain"
PNG_CONTENT_TYPE = "image/png"
