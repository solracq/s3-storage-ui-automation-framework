# Test Strategy

## 1. Purpose

This test strategy defines the overall testing approach for the `Secure S3 File Portal`. It explains the scope, test levels, test types, environments, risks, tools, and quality practices that will be used to validate the frontend implementation of the product.

The current focus is on manual validation of the implemented Phase 1 and Phase 2 portal behavior. Future phases will extend this strategy to include Selenium UI automation, reusable framework utilities, and broader automated regression coverage.

## 2. Test Scope

The scope of this strategy is the frontend behavior of the `Secure S3 File Portal`, validated through the browser and cross-checked through the MinIO console when needed.

### What this validates in the current implementation

* Portal availability through `http://localhost:8000`
* Login and logout behavior for local demo users
* Session-based access to authenticated portal pages
* Health endpoint behavior through `http://localhost:8000/health`
* Storage status display in the UI
* Role-based behavior for `admin` and `viewer`
* File upload, list, download, and delete workflows
* Enforced upload size limit of `1 MB` per file
* File metadata display, including filename, object key, uploaded by, content type, upload date/time, and size
* Flash messages and UI feedback for positive and negative scenarios
* Empty-state behavior
* Page refresh behavior after file actions
* Access denied behavior for unauthorized actions
* Audit log capture and audit log UI visibility
* Seed and reset scripts that support repeatable local validation
* Graceful degraded behavior when MinIO is unavailable
* UI testability through stable `data-testid` attributes
* Cross-browser behavior of important UI workflows

### What is currently out of scope

* Direct backend SDK validation outside the UI
* AWS IAM validation
* Real AWS S3 integration
* Bucket administration workflows not exposed by the portal UI
* Performance, load, and stress testing beyond basic manual observation
* Selenium-based automated execution
* Jenkins-based CI execution

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

* The current implementation includes local demo users: `admin / admin123` and `viewer / viewer123`
* The `admin` role can upload, download, delete, and view audit logs
* The `viewer` role can view and download files but cannot upload, delete, or view audit logs
* The current implementation enforces an upload size limit of `1 MB` per file
* Audit events are persisted locally for authentication, file workflows, and unauthorized access attempts

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
* Authentication and Authorization Testing
* Usability and UI Clarity Testing
* Data Integrity / Metadata Validation
* Reliability and Recovery Testing
* Cross-Browser Testing
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

* Risk 5: Cross-browser differences may affect UI behavior, file upload interaction, or download handling.
  * Occurrence: Medium
  * Severity: Medium
  * Mitigation: Include cross-browser validation for important user workflows and document any browser-specific findings.

* Risk 6: Current implementation limitations may be mistaken for formal requirements.
  * Occurrence: Medium
  * Severity: Medium
  * Mitigation: Distinguish between implemented behavior, known limitations, and future expected product behavior in test documentation.

* Risk 7: Role-based behavior may appear correct in the UI but still require server-side enforcement checks.
  * Occurrence: Medium
  * Severity: High
  * Mitigation: Validate both visual restrictions and direct unauthorized navigation or action attempts.

* Risk 8: File uploads near or above the enforced `1 MB` limit may behave differently across browsers.
  * Occurrence: Medium
  * Severity: Medium
  * Mitigation: Include explicit boundary testing for the enforced upload limit and repeat that coverage in more than one browser when possible.

## 8. Manual and Automation Strategy

The testing approach will be phased.

### Current strategy

* Begin with manual exploratory testing to understand the UI and the product behavior.
* Use the portal UI as the primary validation layer.
* Use the MinIO console as a supporting verification layer for upload and delete actions.
* Use the audit log page as a supporting verification layer for login, file, and unauthorized access events.
* Use the seed and reset scripts to return the environment to a known state when needed.
* Include cross-browser checks for important workflows as part of manual validation.
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

Planned browser coverage:

* Chrome
* Firefox
* Safari, when available in the local environment

## 9. CI/CD Strategy

The long-term target is Jenkins-based execution for the UI automation framework.

Planned CI behavior:

* Build the local application stack
* Start FastAPI and MinIO through Docker Compose
* Run smoke tests first
* Run broader regression and negative suites after smoke passes
* Archive logs, screenshots, and test reports
* Expand CI execution later to include cross-browser coverage where practical

At the current Phase 2 stage, CI automation is planned but not yet implemented.

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
