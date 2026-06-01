# Exploratory Test Document:

## Purpose

Document to show the manual testing activity to understand and validate the `Secure S3 File Portal`.

## Deploying Test Environment

### Using Docker Compose

This method is to deploy the application inside a Docker container:
```bash
docker compose up --build
```
 **Note:**
 The above command will build the app image using `requirements.txt`.

 ### Using uvicorn

 This method will build the app directly on your machine, for a faster code/test iteration.
 ```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.storage_portal.main:app --reload
```

## Endpoints

* FastAPI UI (portal UI): `http://localhost:8000`
* Health endpoint: `http://localhost:8000/health`
* MinIO API: `http://localhost:9000`
* MinIO Console: `http://localhost:9001`

## Testing

The frontend deployment of the product is divide in two parts:
- Phase 1: FastAPI + Jinja2 UI + MinIO integration
- Phase 2: Login, roles, audit entries, seed/reset scripts

Phase 1 has been the only part implemented at the moment, this includes the following:
* FastAPI application scaffold
* Jinja2 dashboard UI for the Secure S3 File Portal
* MinIO-backed upload, list, download, and delete workflows
* Stable `data-testid` attributes on important UI elements
* Docker Compose setup for the portal and MinIO
* `/health` endpoint for basic runtime diagnostics
* Graceful degraded startup when MinIO is unavailable

### Testing Phase 1
Therefore, the exploratory testing of Phase 1 will include the below:
+ Happy-path file workflows, e.g. upload, download and delete file
+ UI clarity and usability
+ File metadata correctness
+ Error/degraded behavior when storage is unavailable -> error messaging clarity
+ Testability of selectors, messages, and page structure
+ Negative scenarios like empty file behaivour, unusual filenames, repeated uploads, and browser refresh after actions

### Testing Approach

* First testing will go through the portal UI, [http://localhost:8000](http://localhost:8000)
* Then use the MinIO console at http://localhost:9001 to confirm backend effects after upload/delete


## Test Scenarios for the Secure S3 File Portal

**Endpoints:**
* Secure S3 File Portal: `http://localhost:8000`
* MinIO Console: `http://localhost:9001`

**App Terminal:**
To deploy and access the `Secure S3 Portal App Terminal`:
```bash
docker compose up --build
```

**Logs:**
```bash
docker logs secure-s3-portal-app
```

### Setup and Pre-requisites
- The `Secure S3 Portal App` has been deployed via docker compose, or directly to a machine.
- The `Secure S3 Portal App Terminal` is available
- A Web browser is open

### Positive Scenarios (happy-path)

#### Scenario 1: Check Portal App Health Endpoint
Go to the `Secure S3 File Portal` and access the health endpoint, `http://localhost:8000/health`

**Output**
```text
{"status":"ok","storage_ready":true,"bucket":"secure-file-portal","storage_error":null}
```
#### Scenario 2: Upload a file
**Pre-requisite:**
- No file has been uploaded on the `Secure S3 File Portal` 

Go to the `Secure S3 File Portal` and upload a file

**Output**
 

#### Scenario 3: Download an uploaded file
**Pre-requisite:**
- A file has been alrady uploaded on the `Secure S3 File Portal`

Go to the `Secure S3 File Portal` and download the file

**Output**


#### Scenario 4: Delete an uploaded file
**Pre-requisite:**
- A file has been alrady uploaded on the `Secure S3 File Portal`

Go to the `Secure S3 File Portal` and delete the file

**Output**


### UI clarity and usability Scenarios

#### Scenario ##: Open Portal App
Access the `Secure S3 File Portal` and verify the following:
- `Secure S3 File Portal` title and descritpion
- Storage status information
- Bucket, endpoint and current mode info
- Choose File and Upload File to Bucket buttons
- Stored Files information 

**Output**
- `Secure S3 File Portal` title is displayed at the top of the page
- A description of the S3 portal is showed
- Storage Status shows `Connected` status
- Bucket name, `secure-file-portal` is shown
- Endpoint, `minio:9000` is displayed
- Current mode, `Phase 1 foundation build`
- Upload File section shows:
  - `Choose File` button
  - No file chosen is indicated, as initial state
  - The upload to secure bucket button is available and clickable
- Stored Files section is displayed:
  - The following columns are shown:
    - FILENAME
    - OBJECT KEY
    - UPLOADED BY
    - CONTENT TYPE
    - UPLOADED AT SIZE
    - ACTIONS
