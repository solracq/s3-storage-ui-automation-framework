# Test Plan

## 1. Test Objectives

The objective of this test plan is to verify and validate that the frontend implementation of the `Secure S3 File Portal` works as expected and supports the intended Phase 1 file workflows.

This test plan focuses on validation through the UI, using the browser as the main interaction point and the MinIO console as a secondary verification point when needed. The plan also prepares the foundation for later Selenium-based automation.

Current objectives:

* Verify that the portal is available and usable through the browser
* Verify that MinIO-backed file workflows operate correctly through the UI
* Verify that file metadata shown in the UI is correct
* Verify that the portal provides clear feedback for positive and negative scenarios
* Verify that the portal degrades gracefully when MinIO is unavailable
* Verify that important UI workflows behave consistently across supported browsers
* Document exploratory findings to support future test automation design

## 2. Entry, Suspension, and Exit Criteria

This section defines the criteria for starting, suspending, and completing the current test cycle.

### 2.1 Entry Criteria

* FastAPI portal is running and reachable at `http://localhost:8000`
* MinIO is running and reachable at `http://localhost:9001`
* Required environment variables and local credentials are configured
* Sample files are available for testing
* Browser access is available
* At least one target browser is available for execution
* `docs/Exploratory_Testing.md` is available as the scenario execution reference

### 2.2 Suspension Criteria

* The portal is unavailable
* MinIO is unavailable for scenarios that require storage access
* Major environment instability prevents reliable execution
* A blocker defect prevents continuation of a large part of the planned scope

### 2.3 Exit Criteria

* Planned Phase 1 exploratory scenarios have been executed
* Critical and high-severity issues are documented
* Results and findings are captured in the exploratory testing document
* Test strategy and test plan are updated to reflect the observed product behavior
* The project is ready to move into the next implementation and automation phases

## 3. Test Resources

The validation of this frontend feature requires the following resources:

* One SDET
* FastAPI `Secure S3 File Portal`
* MinIO local S3-compatible storage
* Docker Compose
* Terminal access
* Web browser
* Sample test files
* MinIO console access

## 4. Test Environment

The test environment for the current implementation includes:

* Local machine
* Docker and Docker Compose
* FastAPI application
* MinIO container
* Modern web browser

### Planned browser coverage

* Primary browser: Chrome
* Secondary browsers for coverage expansion: Firefox and Safari, when available

### Environment details

* Portal UI: `http://localhost:8000`
* Health endpoint: `http://localhost:8000/health`
* MinIO API: `http://localhost:9000`
* MinIO Console: `http://localhost:9001`
* MinIO credentials:
  * Username: `minioadmin`
  * Password: `minioadmin123`

### Optional local app execution

If the portal is run directly with `uvicorn`, MinIO should still be running separately so the portal can connect to storage.

## 5. Scope

### In Scope

The current test cycle includes validation of the Phase 1 frontend implementation:

* Portal page availability and basic usability
* Health endpoint verification
* Storage status visibility
* Empty-state behavior
* File upload workflows
* File download workflow
* File delete workflow
* File metadata validation in the UI
* Positive and negative flash messages
* Browser refresh behavior after actions
* Graceful degraded behavior when MinIO is unavailable
* Cross-checking file actions in the MinIO console
* Cross-browser validation of important UI workflows

### Out of Scope

The following items are out of scope for the current Phase 1 test cycle:

* Login and logout validation
* Session handling validation
* `admin` and `viewer` role validation
* Access denied behavior
* Audit log validation
* Seed and reset script validation
* Real AWS S3 integration
* AWS IAM validation
* Bucket administration actions outside the portal UI
* UI test automation execution

## 6. Test Coverage

The current test coverage is based on the exploratory scenarios documented in `docs/Exploratory_Testing.md`.

### Coverage Areas

* Positive workflows
  * Health endpoint
  * Upload
  * Download
  * Delete

* UI clarity and usability
  * Page title and description
  * Storage status
  * Empty-state messaging
  * Stored file information
  * Available actions
  * Refresh behavior
  * Cross-browser behavior for important page interactions

* Metadata validation
  * File name
  * Object key
  * Uploaded by
  * Content type
  * Uploaded at
  * Size

* Negative validation
  * Upload without selecting a file
  * Upload empty file
  * Upload large file boundary behavior
  * Upload file with non-ASCII characters
  * MinIO unavailable behavior

* Edge validation
  * Unusual or long file names
  * Large file within accepted range
  * Different file types

### Detailed Scenario Reference

Detailed manual scenarios are maintained in:

* `docs/Exploratory_Testing.md`

## 7. Test Data

The test cycle will use:

* Small text files
* Image files
* Empty files
* Files with long names
* Files with non-ASCII characters in the file name
* Different file types
* Larger files for boundary exploration
* More than one browser when available for comparison

## 8. Defect Management

Defects will be documented using GitHub Issues or project notes. Each defect should include:

* Summary
* Steps to reproduce
* Expected result
* Actual result
* Severity
* Logs, screenshots, or supporting notes when applicable

## 9. Schedule and Estimates

This project is being built iteratively, so test work will also be completed in phases.

Planned sequence:

* Phase 1:
  * Manual exploratory testing
  * Test strategy
  * Test plan
  * Exploratory findings review
  * Initial cross-browser observations

* Phase 2:
  * Validation of login, roles, audit entries, and seed/reset behavior
  * Updates to exploratory testing, strategy, and plan documents

* Phase 3:
  * Selenium Page Object Model design
  * Framework utilities
  * Page object implementation

* Phase 4:
  * Smoke automation
  * Regression automation
  * Negative automation
  * CI integration planning and execution
  * Cross-browser automation expansion

## 10. Test Deliverables

### Before testing

* Test plan
* Test strategy
* Environment setup instructions

### During testing

* Exploratory testing notes
* Test scenarios
* Logs
* Screenshots when useful
* Defect reports
* Cross-browser comparison notes, when applicable

### After testing

* Updated exploratory testing document
* Updated test plan
* Updated test strategy
* Execution summary / findings
* Inputs for future Selenium automation design
