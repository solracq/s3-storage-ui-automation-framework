# s3-storage-ui-automation-framework

A small, security-themed web UI built with FastAPI and Jinja2 templates, backed by MinIO/S3-compatible storage. This repository is being built as a Senior SDET portfolio project: first as a practical system under test, and later as a Selenium WebDriver automation framework using Python, Pytest, and the Page Object Model design pattern.

## Current Status

Phase 1 has started with the first implementation slice.

Implemented now:

* FastAPI application scaffold
* Jinja2 dashboard UI for the Secure S3 File Portal
* MinIO-backed upload, list, download, and delete workflows
* Stable `data-testid` attributes on important UI elements
* Docker Compose setup for the portal and MinIO
* `/health` endpoint for basic runtime diagnostics
* Graceful degraded startup when MinIO is unavailable

Not implemented yet:

* Login and logout
* Role-based access for `admin` and `viewer`
* Audit logging
* Seed and reset scripts
* Selenium automation framework
* Smoke, regression, and negative test suites

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

You can also run the FastAPI app locally while keeping MinIO in Docker.

```bash
docker compose up minio
```

# Alternative way to run the application

If the user wants to run the FastAPI app directly on a machine (instead of inside Docker), or if the user wants a faster code/test iteration, then use the method below:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.storage_portal.main:app --reload
```

**Note:**
If MinIO is not running, the app still starts, but the dashboard and `/health` endpoint will show storage as unavailable.

## Endpoints

* FastAPI UI (portal UI): `http://localhost:8000`
* Health endpoint: `http://localhost:8000/health`
* MinIO API: `http://localhost:9000`
* MinIO Console: `http://localhost:9001`

## Target Product Scope

The Secure S3 File Portal is intended to demonstrate:

* User authentication
* Role-based behavior
* File workflows
* Audit logging
* UI testability

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
│       │   └── storage.py
│       ├── routes/
│       │   ├── __init__.py
│       │   └── ui.py
│       ├── services/
│       │   ├── __init__.py
│       │   └── storage.py
│       ├── settings.py
│       ├── static/
│       │   └── styles.css
│       └── templates/
│           ├── base.html
│           └── dashboard.html
├── docker-compose.yml
├── requirements.txt
```
