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
* Smoke, regression, negative, edge, and authentication test coverage with `pytest` and Selenium WebDriver
* Host-based Jenkins pipeline support for running UI tests against the Docker Compose stack

Not implemented yet:

* Fully containerized UI test execution for Selenium
* Jenkins browser matrix or cross-browser CI execution

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
# Usability test suite
.venv/bin/python -m pytest tests/regression/test_usability_regression.py -m usability -vv -s

# Negative test suite
.venv/bin/python -m pytest tests/regression/test_negative_regression.py -m negative -vv -s

# Edge test suite
.venv/bin/python -m pytest tests/regression/test_edge_regression.py -m edge -vv -s

# Authentication test suite
.venv/bin/python -m pytest -m authentication -vv -s
```

**Note:**
Using `.venv/bin/python -m pytest` avoids issues where a globally installed `pytest` points to a different Python interpreter than the local project virtual environment.

## Jenkins CI Approach

The current CI implementation follows:

* `app` and `minio` run through `docker compose`
* Selenium tests run from the Jenkins agent host using a Python virtual environment
* Chrome or Chromium must be installed on the Jenkins agent
* current CI approach: host-based Selenium execution against a Dockerized app stack
* future improvement: fully containerized browser/test execution for higher portability

This keeps the first Jenkins integration simple and reliable while preserving the existing local workflow. The current pipeline definition lives in [Jenkinsfile](.../s3-storage-ui-automation-framework/Jenkinsfile:1).

In Jenkins Stage View, the pipeline now exposes separate test stages for:

* `Smoke Tests`
* `Usability Regression Tests`
* `Negative Regression Tests`
* `Edge Regression Tests`
* `Authentication Tests`

This makes it easier to see which suite area passed, failed, or was skipped during a given run.

### Jenkins Agent Prerequisites

The Jenkins agent should have:

* `python3`
* `docker`
* `docker compose`
* `google-chrome`, `google-chrome-stable`, `chromium-browser`, or `chromium`

On macOS, the pipeline also supports the standard application path:

* `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`

### Start Jenkins Locally

If you are running Jenkins locally on macOS through Homebrew, start the service with:

```bash
brew services start jenkins-lts
```

If you installed the non-LTS formula instead, use:

```bash
brew services start jenkins
```

If you prefer to run Jenkins from a local WAR file with a custom `JENKINS_HOME`, use:

```bash
export JENKINS_HOME="$HOME/jenkins-local/home"
nohup java -jar "$HOME/jenkins-local/war/jenkins.war" --httpPort=8080 \
  > "$HOME/jenkins-local/logs/jenkins.out" 2>&1 &
echo $! > "$HOME/jenkins-local/jenkins.pid"
```

Useful checks:

```bash
brew services list | rg jenkins
```

Jenkins is typically available at:

* `http://localhost:8080`

### Jenkins Test Suite Choices

The pipeline supports these `TEST_SUITE` parameter values:

* `smoke`
* `usability`
* `negative`
* `edge`
* `authentication`
* `all-regression`
* `all-ui`

### Jenkins Reports And Artifacts

The pipeline publishes JUnit XML test reports and archives the `reports/` directory on every run.

This gives you:

* Jenkins `Test Result` details for each build
* the Jenkins `Test Result Trend` graph across builds
* archived artifacts such as:
  * `pytest-*.xml`
  * `docker-compose.log`
  * `docker-compose-ps.txt`
  * `artifact-manifest.txt`

The archived artifacts appear on the Jenkins build page, and the trend graph is driven by the `junit` publication step in the pipeline.

### Jenkins Failure Email Notifications

If `SEND_FAILURE_EMAIL=true` and `EMAIL_RECIPIENTS` is filled in, Jenkins will send an email that includes:

* job name
* build number
* build URL
* test report URL
* artifacts URL

**Note:**
Jenkins must be configured with a working SMTP/mail setup for these notifications to be delivered.

### Local CI-Like Run

If you want to run the same host-based flow locally before wiring Jenkins, use:

```bash
docker compose up -d --build
python3 -m venv .venv-jenkins
.venv-jenkins/bin/python -m pip install --upgrade pip
.venv-jenkins/bin/python -m pip install -r requirements-test.txt
.venv-jenkins/bin/python scripts/wait_for_portal_health.py --base-url http://localhost:8000 --timeout-seconds 90 --require-storage-ready
.venv-jenkins/bin/python scripts/reset_environment.py
.venv-jenkins/bin/python -m pytest tests/smoke -m smoke -vv -s
docker compose down -v
```

### Local Jenkins-Style Suite Commands

Smoke:

```bash
.venv-jenkins/bin/python -m pytest tests/smoke -m smoke -vv -s
```

Usability:

```bash
.venv-jenkins/bin/python -m pytest tests/regression/test_usability_regression.py -m usability -vv -s
```

Negative:

```bash
.venv-jenkins/bin/python -m pytest tests/regression/test_negative_regression.py -m negative -vv -s
```

Edge:

```bash
.venv-jenkins/bin/python -m pytest tests/regression/test_edge_regression.py -m edge -vv -s
```

Authentication:

```bash
.venv-jenkins/bin/python -m pytest -m authentication -vv -s
```

All regression coverage:

```bash
.venv-jenkins/bin/python -m pytest tests/regression -m regression -vv -s
```

All current UI automation:

```bash
.venv-jenkins/bin/python -m pytest tests -m "smoke or regression" -vv -s
```

### Current CI Decision

For now, the project intentionally keeps `pytest` on the Jenkins host instead of in a dedicated test container. This keeps scenario `20` and other Docker-aware tests straightforward, because those tests can control `docker compose` directly from the agent. Full test-container execution can be added later as the next CI maturity step.

## Utility Scripts

Seed the demo users and reset the audit log:

```bash
./.venv/bin/python scripts/seed_demo_users.py
```

Reset stored objects, reseed users, and clear the audit log:

```bash
./.venv/bin/python scripts/reset_environment.py
```

Wait for the portal health endpoint to become ready:

```bash
python3 scripts/wait_for_portal_health.py --base-url http://localhost:8000 --timeout-seconds 90 --require-storage-ready
```

Expected Output:

```bash
{
  "bucket": "secure-file-portal",
  "status": "ok",
  "storage_error": null,
  "storage_ready": true
}
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
├── Jenkinsfile
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
├── pytest.ini
├── requirements-test.txt
├── requirements.txt
├── runtime/  (generated locally)
├── scripts/
│   ├── reset_environment.py
│   ├── seed_demo_users.py
│   └── wait_for_portal_health.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── variables.py
    ├── data/
    │   ├── colors.png
    │   ├── empty.txt
    │   ├── large-file-size-exeeded.txt
    │   ├── large-file.txt
    │   ├── sample-audio.wav
    │   ├── sample-data.csv
    │   ├── sample-document.pdf
    │   ├── sample-no-extension
    │   ├── sample-notes.md
    │   ├── sample-photo.jpeg
    │   ├── sample-report.docx
    │   ├── sdfaflaf;lfad;lkaf;lkfdajk;ljeroijfd98438943%$#YGREW%TS%#HJYJ%JJYTDD%^JJ%S%HTHS.txt
    │   ├── small_file.txt
    │   └── は.txt
    ├── pages/
    │   ├── __init__.py
    │   ├── base_page.py
    │   ├── audit_records/
    │   │   ├── __init__.py
    │   │   └── audit_log_page.py
    │   ├── dashboard/
    │   │   ├── __init__.py
    │   │   └── dashboard_page.py
    │   ├── errors/
    │   │   ├── __init__.py
    │   │   └── access_denied_page.py
    │   └── login/
    │       ├── __init__.py
    │       └── login_page.py
    ├── regression/
    │   ├── test_authentication_regression.py
    │   ├── test_edge_regression.py
    │   ├── test_negative_regression.py
    │   └── test_usability_regression.py
    └── smoke/
        ├── test_admin_login_smoke.py
        ├── test_curated_smoke_scenarios.py
        └── test_positive_file_workflows_smoke.py
```
