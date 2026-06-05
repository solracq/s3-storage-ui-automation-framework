# Test Strategy

## 1. Purpose

This test strategy defines the overall testing approach for the `Secure S3 File Portal`. It explains the scope, test levels, test types, environments, risks, tools, and quality practices that will be used to validate the frontend implementation of the product.

The current focus is on Phase 1 manual validation of the portal UI and the MinIO-backed file workflows. Future phases will extend this strategy to include authentication, roles, audit logging, and Selenium UI automation.

## 2. Test Scope

The scope of this strategy is the frontend behavior of the `Secure S3 File Portal`, validated through the browser and cross-checked through the MinIO console when needed.

### What this validates in the current implementation

* Portal availability through `http://localhost:8000`
* Health endpoint behavior through `http://localhost:8000/health`
* Storage status display in the UI
* File upload, list, download, and delete workflows
* File metadata display, including filename, object key, uploaded by, content type, upload date/time, and size
* Flash messages and UI feedback for positive and negative scenarios
* Empty-state behavior
* Page refresh behavior after file actions
* Graceful degraded behavior when MinIO is unavailable
* UI testability through stable `data-testid` attributes

### What is currently out of scope

* Phase 2 functionality not yet implemented:
  * Login and logout
  * Session handling
  * `admin` and `viewer` roles
  * Access denied behavior
  * Audit logging
  * Seed and reset scripts
* Direct backend SDK validation outside the UI
* AWS IAM validation
* Real AWS S3 integration
* Bucket administration workflows not exposed by the portal UI
* Performance, load, and stress testing beyond basic manual observation

## 3. System Specifications

The system under test is a small local web application that uses MinIO as an S3-compatible storage service.

### System under test

* FastAPI application serving the `Secure S3 File Portal`
* Jinja2 templates for the UI
* MinIO container running locally as the S3-compatible storage service
* Docker Compose for repeatable local execution
* Browser-based interaction with the portal UI
* MinIO console for backend state verification

### Current implementation notes

* The current Phase 1 implementation uses a fixed portal actor: `phase1-demo-admin`
* File workflows are available in the UI today
* Authentication, authorization, and audit behavior are planned for Phase 2

## 4. Roles

Development and QA responsibilities are currently handled by one person in this portfolio project.

* Carlos Quiroz - Software Development Engineer in Test

## 5. Test Levels

The following test levels will guide current and future validation:

* Exploratory Testing: Used first to understand the UI, observe behavior, and identify risks and gaps.
* Smoke Testing: Confirms the portal, MinIO, and health endpoint are available and working at a basic level.
* End-to-End Workflow Testing: Validates UI actions and their resulting storage effects.
* Negative Testing: Validates expected system behavior for invalid or unsupported actions.
* Regression Testing: Re-validates important scenarios after product changes.
* Future Automated UI Testing: Will validate stable user workflows using Selenium WebDriver with Page Object Model.

## 6. Testing Types

The following testing types apply to the current frontend implementation:

* Functional UI Testing
* End-to-End Workflow Testing
* Usability and UI Clarity Testing
* Data Integrity / Metadata Validation
* Reliability and Recovery Testing
* Negative Testing
* Regression Testing

## 7. Risk Analysis

* Risk 1: MinIO may be unavailable or unstable during testing.
  * Occurrence: Medium
  * Severity: High
  * Mitigation: Use the health endpoint, check Docker container status, and include degraded-behavior validation in testing.

* Risk 2: Local Docker or environment issues may affect repeatable execution.
  * Occurrence: Medium
  * Severity: High
  * Mitigation: Use Docker Compose as the baseline setup method and document startup, restart, and troubleshooting steps.

* Risk 3: Persistent MinIO volume data may affect test repeatability.
  * Occurrence: Medium
  * Severity: Medium
  * Mitigation: Start scenarios from a known state when required and document when environment cleanup is needed.

* Risk 4: Browser download behavior may vary by machine or browser settings.
  * Occurrence: Medium
  * Severity: Medium
  * Mitigation: Validate downloads using the browser and local filesystem expectations, and document browser assumptions.

* Risk 5: Current implementation limitations may be mistaken for formal requirements.
  * Occurrence: Medium
  * Severity: Medium
  * Mitigation: Distinguish between implemented behavior, known limitations, and future expected product behavior in test documentation.

## 8. Manual and Automation Strategy

The testing approach will be phased.

### Current strategy

* Begin with manual exploratory testing to understand the UI and the product behavior.
* Use the portal UI as the primary validation layer.
* Use the MinIO console as a supporting verification layer for upload and delete actions.
* Record findings in `docs/Exploratory_Testing.md`.
* Use exploratory findings to drive the test plan, test strategy, and future automated coverage.

### Future automation strategy

Automated tests will be implemented in Python using:

* Selenium WebDriver
* Pytest
* Page Object Model

Planned suite structure:

* `tests/smoke/`
* `tests/regression/`
* `tests/negative/`

Planned automation utilities:

* Driver factory
* Explicit waits
* Screenshot capture
* Test data helpers
* Reusable page objects

## 9. CI/CD Strategy

The long-term target is Jenkins-based execution for the UI automation framework.

Planned CI behavior:

* Build the local application stack
* Start FastAPI and MinIO through Docker Compose
* Run smoke tests first
* Run broader regression and negative suites after smoke passes
* Archive logs, screenshots, and test reports

At the current Phase 1 stage, CI automation is planned but not yet implemented.

## 10. Test Logistics

The current validation of the product is manual and exploratory, executed locally by one SDET.

Current logistics:

* Execute the product locally through Docker Compose
* Run exploratory scenarios through the browser
* Use MinIO console verification where helpful
* Capture findings in the exploratory testing document
* Refine test plan and test strategy before starting UI automation

Reference document:

* `docs/Exploratory_Testing.md`
