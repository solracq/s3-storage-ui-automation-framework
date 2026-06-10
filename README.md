# s3-storage-ui-automation-framework

A small, security-themed web UI built with FastAPI and Jinja2 templates, backed by MinIO/S3-compatible storage. This repository is being built as a Senior SDET portfolio project: first as a practical system under test, and later as a Selenium WebDriver automation framework using Python, Pytest, and the Page Object Model design pattern.

## Current Status

Phase 1 and Phase 2 are now implemented in the local MVP.

Implemented now:

* FastAPI application scaffold
* Jinja2 dashboard UI for the Secure S3 File Portal
* MinIO-backed upload, list, download, and delete workflows
* Login and logout flows for local demo users
* Role-based access for `admin` and `viewer`
* Session handling for authenticated portal access
* Audit logging for login, file, and unauthorized access events
* Audit log UI page for the `admin` user
* Seed and reset scripts for repeatable local testing
* Stable `data-testid` attributes on important UI elements
* Docker Compose setup for the portal and MinIO
* `/health` endpoint for basic runtime diagnostics
* Graceful degraded startup when MinIO is unavailable
* Initial Selenium Page Object Model structure
* Initial smoke test coverage with `pytest` and Selenium WebDriver

Not implemented yet:

* Broader regression and negative automated test suites
* CI execution for UI automation

## Planned Roadmap

* Phase 1: FastAPI + Jinja2 UI + MinIO integration
* Phase 2: Login, roles, audit entries, seed/reset scripts
* Phase 3: Selenium Page Object Model framework
* Phase 4: Smoke, regression, and negative automated tests

## Quick Start

It is recommended to run the full local stack with Docker Compose. This method builds the app image from Dockerfile using `requirements.txt`, the `app` container already starts `uvicorn` and compose also starts `MinIO`.

```bash
docker compose up --build
```

This starts:

* FastAPI UI on `http://localhost:8000`
* MinIO API on `http://localhost:9000`
* MinIO Console on `http://localhost:9001`

Demo credentials:

* `admin / admin123`
* `viewer / viewer123`

You can also run the FastAPI app locally while keeping MinIO in Docker.

```bash
docker compose up minio
```

## Alternative Local Run

If you want to run the FastAPI app directly on your machine instead of inside Docker, or if you want a faster code/test iteration loop, use the method below:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.storage_portal.main:app --reload
```

**Note:**
If MinIO is not running, the app still starts, but the dashboard and `/health` endpoint will show storage as unavailable.

## Local Smoke Test Run

To run the current Selenium smoke tests locally, first make sure the portal stack is already running at `http://localhost:8000`.

If you have not created the local virtual environment yet:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-test.txt
```

Then run the smoke suites with:

```bash
.venv/bin/python -m pytest tests/smoke/test_admin_login_smoke.py -m smoke -vv -s
.venv/bin/python -m pytest tests/smoke/test_positive_file_workflows_smoke.py -m smoke -vv -s
.venv/bin/python -m pytest tests/smoke/test_curated_smoke_scenarios.py -m smoke -vv -s
```

Run all smoke tests
```bash
.venv/bin/python -m pytest tests/smoke -m smoke -vv -s
```

## Local Regression Test Run
```bash
.venv/bin/python -m pytest tests/regression/test_usability_regression.py -m usability -vv -s
```

**Note:**
Using `.venv/bin/python -m pytest` avoids issues where a globally installed `pytest` points to a different Python interpreter than the local project virtual environment.

## Utility Scripts

Seed the demo users and reset the audit log:

```bash
./.venv/bin/python scripts/seed_demo_users.py
```

Reset stored objects, reseed users, and clear the audit log:

```bash
./.venv/bin/python scripts/reset_environment.py
```

## Endpoints

* FastAPI UI (portal UI): `http://localhost:8000` -> This redirects unauthenticated users to the login page and serves the Secure S3 File Portal after sign-in.
* Health endpoint: `http://localhost:8000/health` -> This returns JSON such as `"status":"ok"` and `"bucket":"secure-file-portal"`
* MinIO API: `http://localhost:9000`
* MinIO Console: `http://localhost:9001` -> This should show bucket information and contents

## Current MVP Constraints

* This project uses local demo credentials only. It does not use AWS IAM or real AWS services.
* The portal currently enforces a local upload limit of `1 MB` per file and returns a clear validation message when that limit is exceeded.
* The current demo user store and audit log are file-based under `runtime/` to keep the project simple and repeatable for local testing.

## Target Product Scope

The Secure S3 File Portal is intended to demonstrate:

* User authentication
* Role-based behavior
* File workflows
* Audit logging
* UI testability
* Repeatable local environment setup and reset workflows
* A future Selenium Page Object Model automation layer

## Logs

If you need application logs during local deployment or debugging, use:

```bash
docker logs secure-s3-portal-app
```

## Current Repository Structure

```text
s3-storage-ui-automation-framework/
├── Dockerfile
├── README.md
├── app/
│   ├── __init__.py
│   └── storage_portal/
│       ├── __init__.py
│       ├── main.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── audit.py
│       │   ├── auth.py
│       │   └── storage.py
│       ├── routes/
│       │   ├── __init__.py
│       │   └── ui.py
│       ├── services/
│       │   ├── __init__.py
│       │   ├── audit.py
│       │   ├── auth.py
│       │   └── storage.py
│       ├── settings.py
│       ├── static/
│       │   └── styles.css
│       └── templates/
│           ├── access_denied.html
│           ├── audit_log.html
│           ├── base.html
│           ├── dashboard.html
│           └── login.html
├── docs/
│   ├── Exploratory_Testing.md
│   ├── Test_Plan_s3_storage_UI.md
│   └── Test_Strategy_s3_storage_UI.md
├── docker-compose.yml
├── requirements.txt
├── runtime/  (generated locally)
└── scripts/
    ├── reset_environment.py
    └── seed_demo_users.py
```
