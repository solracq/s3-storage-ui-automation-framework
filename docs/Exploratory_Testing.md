# Exploratory Testing Document

## Purpose

This document records the manual exploratory testing activity used to understand and validate the `Secure S3 File Portal`.

## Deploying the Test Environment

### Using Docker Compose

Use this method to deploy the application and MinIO in Docker containers:

```bash
docker compose up --build
```

**Note:** This command builds the app image using `requirements.txt`.

### Using `uvicorn`

Use this method to run the application directly on your machine for faster code and test iteration.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.storage_portal.main:app --reload
```

**Note:** When using this method, MinIO should still be running separately so the portal can connect to storage.

## Endpoints

* FastAPI UI (portal UI): `http://localhost:8000`
* Health endpoint: `http://localhost:8000/health`
* MinIO API: `http://localhost:9000`
* MinIO Console: `http://localhost:9001`

## Testing Scope

The frontend deployment of the product is divided into two parts:

* Phase 1: FastAPI + Jinja2 UI + MinIO integration
* Phase 2: Login, roles, audit entries, seed/reset scripts

At the moment, Phase 1 and Phase 2 have been implemented. They include the following:

* FastAPI application scaffold
* Jinja2 dashboard UI for the Secure S3 File Portal
* MinIO-backed upload, list, download, and delete workflows
* Stable `data-testid` attributes on important UI elements
* Docker Compose setup for the portal and MinIO
* `/health` endpoint for basic runtime diagnostics
* Graceful degraded startup when MinIO is unavailable
* Login and logout flows for local demo users
* Session handling for authenticated portal access
* Role-based behavior for `admin` and `viewer`
* Access denied handling for unauthorized actions
* Audit log capture and audit log UI visibility
* Seed and reset scripts for repeatable local testing

### Testing Phase 1 and Phase 2

The exploratory testing for Phase 1 and Phase 2 includes the following areas:

* Happy-path file workflows such as upload, download, and delete
* Authentication and invalid credential combinations
* Role-based UI behavior for `admin` and `viewer`
* UI clarity, messages, page structure, and usability scenarios
* File metadata correctness
* Negative scenarios such as empty file behavior, invalid credentials, unusual filenames, repeated uploads, and browser refresh after actions
* Audit logging visibility and unauthorized access behavior
* Credential entry methods such as typing, copy-pasting, and auto-fill when applicable
* Edge scenarios
* Cross-browser validation

### Testing Approach

* First, perform testing through the portal UI at [http://localhost:8000](http://localhost:8000).
* Then, use the MinIO console at `http://localhost:9001` to confirm backend effects after upload and delete actions.
* When possible, repeat important portal scenarios in more than one browser to observe browser-specific behavior.

## Test Scenarios for the Secure S3 File Portal

**Endpoints**

* Secure S3 File Portal: `http://localhost:8000`
* MinIO Console: `http://localhost:9001`

**App Terminal**

To start the `Secure S3 Portal App`:

```bash
docker compose up --build
```

**Logs**

```bash
docker logs secure-s3-portal-app
```

### Setup and Prerequisites

* The `Secure S3 Portal App` has been deployed via Docker Compose or directly on a machine.
* The `Secure S3 Portal App` terminal is available.
* A web browser is open.
* The demo credentials are available:
  * `admin / admin123`
  * `viewer / viewer123`

### Positive Scenarios (Happy Path)

#### Scenario 1: Check Portal App Health Endpoint

1. Go to the `Secure S3 File Portal`.
2. Access the health endpoint at `http://localhost:8000/health`.

**Output**

```text
{"status":"ok","storage_ready":true,"bucket":"secure-file-portal","storage_error":null}
```

#### Scenario 2: Upload a file by selecting a file

**Prerequisite**

* No file has been uploaded to the `Secure S3 File Portal`.
* Sign in as `admin`.

1. Go to the `Secure S3 File Portal`.
2. Upload a file by clicking the `Choose File` button in the `Upload File` section of the portal.
3. Click the `Upload to Secure Bucket` button to upload the file to the bucket.
4. Verify that the new file has been uploaded.

**Output**

2) The file is successfully selected, and its name is displayed in the upload section.
3) A `File uploaded successfully.` message is displayed in the File Portal.
3) The `Stored Files` section shows the correct uploaded file name, content type, uploaded date and time, and file size.
4) The uploaded file appears in the MinIO console.

#### Scenario 3: Upload a file by dragging the file

**Prerequisite**

* No file has been uploaded to the `Secure S3 File Portal`.
* Sign in as `admin`.

1. Go to the `Secure S3 File Portal`.
2. Upload a file by dragging it into the `Upload File` section of the portal.
3. Click the `Upload to Secure Bucket` button to upload the file to the bucket.
4. Verify that the new file has been uploaded.

**Output**

2) The file is successfully selected, and its name is displayed in the upload section.
3) A `File uploaded successfully.` message is displayed in the File Portal.
3) The `Stored Files` section shows the correct uploaded file name, content type, uploaded date and time, and file size.
4) The uploaded file appears in the MinIO console.

#### Scenario 4: Download an uploaded file

**Prerequisite**

* A file has already been uploaded to the `Secure S3 File Portal`.
* Sign in as `admin` or `viewer`.

1. Go to the `Secure S3 File Portal`.
2. Select and download the existing file.

**Output**

2) The user is able to download the file to the specified location.
2) The file can be opened and viewed.

#### Scenario 5: Delete an uploaded file

**Prerequisites**

* A file has already been uploaded to the `Secure S3 File Portal`.
* The uploaded file is displayed in the `Stored Files` section of the portal.
* Sign in as `admin`.

1. Go to the `Secure S3 File Portal`.
2. Delete the file by clicking the `Delete` button.
3. Verify that the file appears deleted in both the File Portal and the MinIO console.

**Output**

3) A `File deleted successfully.` message appears in the File Portal.
3) The file information is no longer available in the `Stored Files` section of the portal.
3) The file is no longer available in the MinIO console.

### UI Clarity, Messages, Page Structure, and Usability Scenarios

#### Scenario 6: Open the Portal App

**Prerequisite**

* Secure S3 File Portal initial state with no previously uploaded files.
* Sign in as `admin`.

Access the `Secure S3 File Portal` and verify the following:

* `Secure S3 File Portal` title and description
* Storage status information
* Bucket, endpoint, and current mode information
* `Choose File` and `Upload to Secure Bucket` buttons
* `Stored Files` information

**Output**

* The `Secure S3 File Portal` title is displayed at the top of the page.
* A description of the portal is shown.
* `Storage Status` shows `Connected`.
* The bucket name `secure-file-portal` is shown.
* The endpoint `minio:9000` is displayed.
* The current mode `Phase 2 access-control build` is displayed.
* The `Upload File` section shows:
  * A `Choose File` button
  * `No file chosen` as the initial/default state
  * A `Maximum upload size: 1 MB per file.` note
  * An `Upload to Secure Bucket` button that is available and clickable
* The `Stored Files` section is displayed with the following columns:
  * `FILENAME`
  * `OBJECT KEY`
  * `UPLOADED BY`
  * `CONTENT TYPE`
  * `UPLOADED AT`
  * `SIZE`
  * `ACTIONS`

#### Scenario 7: Verify the initial `Stored Files` status in the File Portal

**Prerequisite**

* Secure S3 File Portal initial state with no previously uploaded files.
* Sign in as `admin`.

1. Go to the `Secure S3 File Portal`.
2. Check the `Stored Files` section.
3. Check the MinIO console.

**Output**

2) The following message is displayed: `No files are stored yet. Upload a sample object to verify the MinIO integration end to end.`
2) & 3) No files are shown in either the File Portal or the MinIO console.

#### Scenario 8: Verify the uploaded file name and extension in the File Portal

**Prerequisite**

* Secure S3 File Portal initial state with no previously uploaded files.
* Sign in as `admin`.

1. Go to the `Secure S3 File Portal`.
2. Upload a file.
3. Verify that the file name shown in `Stored Files` matches the actual uploaded file name and extension.

**Output**

3) The file name shown in the portal matches the file name that was uploaded.

#### Scenario 9: Verify the object key correctness of an uploaded file in the File Portal

**Prerequisite**

* Secure S3 File Portal initial state with no previously uploaded files.
* Sign in as `admin`.

1. Go to the `Secure S3 File Portal`.
2. Upload a file.
3. Verify that the object key shown in `Stored Files` is correct.

**Output**

3) The object key should contain the following:
   - The upload folder
   - The upload date
   - Random characters
   - The file name and extension

#### Scenario 10: Verify the `uploaded by` information of the uploaded file

**Prerequisite**

* Secure S3 File Portal initial state with no previously uploaded files.
* Sign in as `admin`.

1. Go to the `Secure S3 File Portal`.
2. Upload a file.
3. Verify that the `uploaded by` information matches the currently signed-in upload user.

**Output**

3) The uploaded file shows `admin` in the `uploaded by` column.

#### Scenario 11: Verify the content type of the uploaded file in the File Portal

**Prerequisite**

* Secure S3 File Portal initial state with no previously uploaded files.
* Sign in as `admin`.

1. Go to the `Secure S3 File Portal`.
2. Upload a text file and an image.
3. Verify that the files appear in `Stored Files` and that their content types match the actual uploaded objects.

**Output**

3) The content type shown in the portal matches the content type of the uploaded file.
3) The content type is shown in the format `type/subtype`.

#### Scenario 12: Verify the `uploaded at` information of the uploaded file

**Prerequisite**

* Secure S3 File Portal initial state with no previously uploaded files.
* Sign in as `admin`.

1. Go to the `Secure S3 File Portal`.
2. Upload a file.
3. Verify that the `uploaded at` information shown in `Stored Files` matches the upload time.

**Output**

3) The `Stored Files` section shows when the file was uploaded.
3) The information is shown in the format `Date - Time - Time Zone`.

#### Scenario 13: Verify the `size` information of the uploaded file

**Prerequisite**

* Secure S3 File Portal initial state with no previously uploaded files.
* Sign in as `admin`.

1. Go to the `Secure S3 File Portal`.
2. Upload a file.
3. Verify that the `size` information shown in `Stored Files` matches the uploaded file size.

**Output**

3) The `Stored Files` section shows the correct file size.

#### Scenario 14: Verify the `Actions` information in the File Portal

**Prerequisite**

* Secure S3 File Portal initial state with no previously uploaded files.
* Sign in as `admin`.

1. Go to the `Secure S3 File Portal`.
2. Upload a file.
3. Verify the available actions shown in `Stored Files`.

**Output**

3) The available actions for the uploaded file are `Download` and `Delete`.
3) Both `Download` and `Delete` are clickable.

#### Scenario 15: Refresh the File Portal page after uploading or deleting a file

**Prerequisite**

* Secure S3 File Portal initial state with no previously uploaded files.
* Sign in as `admin`.

1. Go to the `Secure S3 File Portal`.
2. Upload a file.
3. Refresh the browser page.
4. Verify that the uploaded file information still appears correctly in `Stored Files`.
5. Delete the file.
6. Refresh the browser page.
7. Verify that the file no longer appears in `Stored Files`.

**Output**

2) & 4) The uploaded file information still appears correctly in `Stored Files`.
5) & 7) No information about the deleted file remains in `Stored Files`.

### Negative Scenarios

#### Scenario 16: Attempt to upload a file without selecting one

**Prerequisite**

* Secure S3 File Portal initial state with no previously uploaded files.
* Sign in as `admin`.

1. Go to the `Secure S3 File Portal`.
2. Without choosing a file, click the upload button.
3. Verify that no file is uploaded and that the appropriate error message is displayed.

**Output**

3) No file is uploaded.
3) The error message `Please choose a file before uploading.` is displayed.

#### Scenario 17: Upload an empty file

**Prerequisite**

* Secure S3 File Portal initial state with no previously uploaded files.
* Sign in as `admin`.

1. Go to the `Secure S3 File Portal`.
2. Upload an empty file.
3. Verify that the file cannot be uploaded.

**Output**

3) No file is uploaded.
3) The error message `Please upload a non-empty file.` is displayed.

#### Scenario 18: Upload a large file exceeding the allowed limit (more than 1 MB)

**Prerequisite**

* Secure S3 File Portal initial state with no previously uploaded files.
* Sign in as `admin`.

1. Go to the `Secure S3 File Portal`.
2. Upload a large file that exceeds the allowed limit (more than 1 MB).
3. Verify that the file cannot be uploaded.

**Output**

3) No file is uploaded.
3) The error message `Maximum upload size exceeded. This portal currently supports files up to 1 MB.` is displayed.

#### Scenario 19: Upload a file with non-ASCII characters in the file name

**Prerequisite**

* Secure S3 File Portal initial state with no previously uploaded files.
* Sign in as `admin`.

1. Go to the `Secure S3 File Portal`.
2. Upload a file with non-ASCII characters in the file name, for example `こんにちは`.
3. Verify that the file cannot be uploaded.

**Output**

3) The file cannot be uploaded.
3) The error message `unsupported metadata value こんにちは.txt; only US-ASCII encoded characters are supported` is displayed.

#### Scenario 20: Verify File Portal behavior when MinIO is unavailable

**Prerequisite**

* The `Secure S3 Portal App` is running.
* MinIO has been stopped or is unavailable.
* Sign in as `admin` or `viewer`.

1. Stop the MinIO service or make MinIO unavailable.
2. Go to the `Secure S3 File Portal`.
3. Access the health endpoint at `http://localhost:8000/health`.
4. Verify the storage status shown in the portal.

**Output**

2) The `Secure S3 File Portal` remains accessible.
3) The health endpoint returns a degraded response with `storage_ready` set to `false`.
4) The portal shows `Unavailable` in the `Storage Status` section.
4) A storage error message is displayed in the portal.

### Edge Scenarios

#### Scenario 21: Upload a file with an unusual or long file name

**Prerequisite**

* Secure S3 File Portal initial state with no previously uploaded files.
* Sign in as `admin`.

1. Go to the `Secure S3 File Portal`.
2. Upload a file with an unusual or long name.
3. Verify that the file can be uploaded.

**Output**

3) The file can be uploaded successfully.
3) The file name and object key with the unusual or long characters are displayed correctly in the File Portal.

#### Scenario 22: Upload a large file within the allowed limit (<= 1 MB)

**Prerequisite**

* Secure S3 File Portal initial state with no previously uploaded files.
* Sign in as `admin`.

1. Go to the `Secure S3 File Portal`.
2. Upload a large file within the allowed limit (`<= 1 MB`).
3. Verify that the file can be uploaded in both the File Portal and the MinIO console.

**Output**

3) The file can be uploaded successfully in the File Portal.
3) The file is displayed in the MinIO console.

#### Scenario 23: Upload different file types

**Prerequisite**

* Secure S3 File Portal initial state with no previously uploaded files.
* Sign in as `admin`.

1. Go to the `Secure S3 File Portal`.
2. Upload different file types (`txt`, `pdf`, `docx`, `csv`, `jpeg`, `png`, `mp4`, `wav`, `md`, and files without an extension).
3. Verify that all file types can be uploaded in both the File Portal and the MinIO console.

**Output**

3) The files can be uploaded successfully in the File Portal.
3) The files are displayed in the MinIO console.

### Phase 2 Authentication, Role, and Credential Handling Scenarios

#### Scenario 24: Attempt to log in as `admin` using the correct username and the wrong password, and vice versa

**Prerequisite**

* The `Secure S3 File Portal` login page is accessible.

1. Go to the `Secure S3 File Portal` login page.
2. Enter the correct `admin` username and an incorrect password, then submit.
3. Enter an incorrect `admin` username and the correct password, then submit.
4. Verify that access to the portal is denied in both cases.

**Output**

2) The login is unsuccessful.
2) The error message `Invalid username or password.` is displayed.
3) The login is unsuccessful.
3) The error message `Invalid username or password.` is displayed.
4) The user remains blocked from the portal dashboard in both attempts.

#### Scenario 25: Attempt to log in as `viewer` using the correct username and the wrong password, and vice versa

**Prerequisite**

* The `Secure S3 File Portal` login page is accessible.

1. Go to the `Secure S3 File Portal` login page.
2. Enter the correct `viewer` username and an incorrect password, then submit.
3. Enter an incorrect `viewer` username and the correct password, then submit.
4. Verify that access to the portal is denied in both cases.

**Output**

2) The login is unsuccessful.
2) The error message `Invalid username or password.` is displayed.
3) The login is unsuccessful.
3) The error message `Invalid username or password.` is displayed.
4) The user remains blocked from the portal dashboard in both attempts.

#### Scenario 26: Validate credential input methods on the login page

**Prerequisite**

* The `Secure S3 File Portal` login page is accessible.

1. Enter valid credentials by typing them on the keyboard and submit.
2. Log out.
3. Enter valid credentials by copy-pasting them into the username and password fields and submit.
4. Log out.
5. If the browser provides auto-fill for the login fields, use it to populate the credentials and submit.

**Output**

1) The portal accepts credentials entered by typing and allows successful login.
3) The portal accepts credentials entered by copy-pasting and allows successful login.
5) If auto-fill is available in the browser, the portal accepts the auto-filled credentials and allows successful login.
5) If auto-fill is not available in the browser, the scenario is marked as not applicable.

#### Scenario 27: Validate buttons, links, control icons, badges, and text for the `admin` role

**Prerequisite**

* Sign in as `admin`.

1. Go to the `Secure S3 File Portal`.
2. Review the top bar, dashboard panels, upload section, and file actions.
3. Verify that the `admin` role sees the expected buttons, links, control icons, badges, and descriptive text.

**Output**

2) The top bar shows `Dashboard`, `Audit Log`, the current user badge, and the `Logout` button.
2) The dashboard shows the `Upload File` section with the `Choose File` and `Upload to Secure Bucket` controls.
2) The dashboard shows the upload note `Maximum upload size: 1 MB per file.`
3) The `Stored Files` section shows `Download` and `Delete` actions for the `admin` role.
3) The page text reflects the signed-in `admin` user and the `admin` role.
3) The available controls are visible, readable, and clickable.

#### Scenario 28: Validate buttons, links, control icons, badges, and text for the `viewer` role

**Prerequisite**

* Sign in as `viewer`.

1. Go to the `Secure S3 File Portal`.
2. Review the top bar, dashboard panels, and file actions.
3. Verify that the `viewer` role sees only the allowed buttons, links, control icons, badges, and descriptive text.

**Output**

2) The top bar shows `Dashboard`, the current user badge, and the `Logout` button.
2) The `Audit Log` link is not shown for the `viewer` role.
2) The dashboard shows the `Viewer Access` panel instead of the upload section.
3) The `Stored Files` section shows the `Download` action only.
3) The `Delete` action is not displayed for the `viewer` role.
3) The page text reflects the signed-in `viewer` user and the `viewer` role.

#### Scenario 29: Attempt to access protected portal pages without authentication

**Prerequisite**

* No active portal session is present.

1. Go directly to the Secure S3 File Portal root URL.
2. Attempt to access the audit log URL directly without logging in.
3. Verify that both protected routes redirect the user to the login page.

**Output**

2) The unauthenticated user is redirected to the login page.
2) The message `Please sign in to access the portal.` is displayed when access is blocked.

#### Scenario 30: Log out and verify that the session is invalidated

**Prerequisite**

* Sign in as `admin` or `viewer`.

1. Go to the Secure S3 File Portal.
2. Click the `Logout` button.
3. Attempt to return to the dashboard by using the browser navigation or by entering the dashboard URL directly.
4. Verify that the session no longer grants access to the protected portal pages.

**Output**

2) The user is returned to the login page.
2) The message `Logged out successfully.` is displayed.
3) The user is redirected to the login page instead of the dashboard.
4) The session no longer grants access to the protected portal pages.
