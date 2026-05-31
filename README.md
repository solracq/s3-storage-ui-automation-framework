# s3-storage-ui-automation-framework

A small, security-themed web UI built with FastAPI and Jinja2 templates, backed by MinIO/S3-compatible storage. Including a test automation framework for the UI using Selenium WebDriver with Python, Pytest, and the Page Object Model design pattern

## Current Status

Phase 1 is now started with the first implementation slice:

* FastAPI application scaffold
* Jinja2 security-themed dashboard UI
* MinIO-backed file upload, list, download, and delete workflows
* Stable `data-testid` attributes on important UI elements
* Docker Compose setup for the portal and MinIO

Authentication, role-based access, audit logging, seed scripts, and reset scripts are intentionally deferred to Phase 2.

## Quick Start

Install dependencies locally:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.storage_portal.main:app --reload
```

Or run with Docker Compose:

```bash
docker compose up --build
```

Endpoints:

* FastAPI UI: `http://localhost:8000`
* MinIO API: `http://localhost:9000`
* MinIO Console: `http://localhost:9001`

This “Secure S3 File Portal” will contain the following functionality:
* User authentication
* Role-based behavior
* File workflows
* Audit logging
* UI testability

# Initial Folder Structure
```text
s3-storage-ui-automation-framework/
├── app/
│   └── storage_portal/
│       ├── __init__.py
│       ├── main.py
│       ├── settings.py
│       ├── routes/
│       ├── templates/
│       ├── static/
│       │   └── styles.css
│       ├── models/
│       └── auth/
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   ├── login_page.py
│   ├── dashboard_page.py
│   ├── upload_page.py
│   ├── files_page.py
│   └── audit_log_page.py
├── tests/
│   ├── conftest.py
│   ├── smoke/
│   ├── regression/
│   └── negative/
├── utils/
├── docs/
├── reports/
├── screenshots/
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```
