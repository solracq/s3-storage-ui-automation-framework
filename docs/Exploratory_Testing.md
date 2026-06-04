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
+ UI clarity, Messages, Page Structure and usability Scenarios
+ File metadata correctness
+ Error/degraded behavior when storage is unavailable -> error messaging clarity
+ Negative scenarios like empty file behaivour, unusual filenames, repeated uploads, and browser refresh after actions
+ Edge scenarios

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


### Positive Scenarios (Happy-Path)

#### Scenario 1: Check Portal App Health Endpoint
1) Go to the `Secure S3 File Portal` 
2) Access the health endpoint, `http://localhost:8000/health`

**Output**
```text
{"status":"ok","storage_ready":true,"bucket":"secure-file-portal","storage_error":null}
```
#### Scenario 2: Upload a file
**Pre-requisite:**
- No file has been uploaded on the `Secure S3 File Portal` 

1) Go to the `Secure S3 File Portal` 
2) Upload a file by clicking the Choose File button under the Upload File section of the File Porta. 
3) Click on the Upload to Secure Bucket button to upload the file into the bucket. 
4) Verify the new file has been uploaded.

**Output**
 2) File is sucessfully selected and title displayed in the upload file section.
 3) File upladed successfully message displayed in File Portal.
 3) The Stored Files section shows the correct uploaded file name, content type, uploaded date/time, and file size.
 4) Upladed file appears in the MinIO console.

#### Scenario 3: Download an uploaded file
**Pre-requisite:**
- A file has been alrady uploaded on the `Secure S3 File Portal`

1) Go to the `Secure S3 File Portal` 
2) Select and download the existing file

**Output**
2) User is able to download the file to the specified location
3) File can be opened and viewed

#### Scenario 4: Delete an uploaded file
**Pre-requisite:**
- A file has been alrady uploaded on the `Secure S3 File Portal`
- Uploaded file is displayed in the Stored Files section of the portal

1) Go to the `Secure S3 File Portal`
2) Select and delete the file by clikcing the delete button. 
3) Vefify the file appears deleted in the File Portal and in the MinIO console.

**Output**
3) File deleted successfully message appears in the File Portal
3) File information is no loner available in the Stored Files section of the portal
3) File is no longer available in the MinIO console

### UI clarity, Messages, Page Structure and usability Scenarios

#### Scenario 5: Open Portal App
**Pre-requisite:**
- Secure S3 File Portal initial state (no file has been uploaded previously)

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
    - No file chosen is indicated as initial/default state
  - The upload to secure bucket button is available and clickable
- Stored Files section is displayed:
  - The following columns are shown:
    - FILENAME
    - OBJECT KEY
    - UPLOADED BY
    - CONTENT TYPE
    - UPLOADED AT
    - SIZE
    - ACTIONS

#### Scenario 6: Verify Stored Files Initial Status in Fle Portal.
**Pre-requisite:**
- Secure S3 File Portal initial state (no file has been uploaded previously)

1) Go to the `Secure S3 File Portal` 
2) Check the Stored Files section
3) Check the MinIO console

**Output**
 2) The following message is displayed: No files are stored yet. Upload a sample object to verify the MinIO integration end to end.
 2) & 3) No files are shown

#### Scenario 7: Verify the name and extension of the upoaded file match with the name and extension in the Fle Portal.
**Pre-requisite:**
- Secure S3 File Portal initial state (no file has been uploaded previously)

1) Go to the `Secure S3 File Portal` 
2) Upload a file with filename. 
3) Verify the filename that appears in the File Portal > Stored Files section matches with the actual filename of the object uploaded.

**Output**
 3) Filename of the uploaded file in Portal matches with the filename uploaded earlier.

#### Scenario 8: Verify the object key correctness of an uploaded file in the Fle Portal.
**Pre-requisite:**
- Secure S3 File Portal initial state (no file has been uploaded previously)

1) Go to the `Secure S3 File Portal` 
2) Upload a file.
3) Verify the object key name that appears in the File Portal > Stored Files section is correct

**Output**
 3) Object key should contain the following:
    - upload folder
    - upload date
    - random characters
    - filename and extension 

#### Scenario 9: Verify the 'uploadad by' information of the upoaded file matches with the Fle Portal's username.
**Pre-requisite:**
- Secure S3 File Portal initial state (no file has been uploaded previously)

1) Go to the `Secure S3 File Portal` 
2) Upload a file
3) Verify the 'uploaded by' information matches the current username in the portal.

**Output**
 3) The uploaded file shows in the 'uploaded' column the current username in the portal.

#### Scenario 10: Verify the content type of the upoaded file matches with the content type in the Fle Portal.
**Pre-requisite:**
- Secure S3 File Portal initial state (no file has been uploaded previously)

1) Go to the `Secure S3 File Portal` 
2) Upload a text file and an image 
3) Verify the files appear in the File Portal > Stored Files section and their content type matches with the actual content type of the object uploaded.

**Output**
 3) Content type of the uploaded file in Portal matches with the content types uploaded earlier.
 3) Content type in file portal is shwon in the following format: "file_type / file_extension"

#### Scenario 11: Verify the 'uploadad at' information of the upoaded file matches with the File Portal's date/time.
**Pre-requisite:**
- Secure S3 File Portal initial state (no file has been uploaded previously)

1) Go to the `Secure S3 File Portal` 
2) Upload a file
3) Verify the 'uploaded at' information in the File Portal > Stored Files section matches with the file was uploaded.

**Output**
 3) The Stored Files section shows information about when the file was uploaded in the portal.
 3) The information is shown in the following format: Date - Time - TimeZone

#### Scenario 12: Verify the 'size' information of the upoaded file matches with the file size in File Portal.
**Pre-requisite:**
- Secure S3 File Portal initial state (no file has been uploaded previously)

1) Go to the `Secure S3 File Portal` 
2) Upload a file
3) Verify the 'size' information in the File Portal > Stored Files section matches with the uploaded file size.

**Output**
 3) The Stored Files section shows information about when the file size.

#### Scenario 13: Verify the 'Actions' information in File Portal.
**Pre-requisite:**
- Secure S3 File Portal initial state (no file has been uploaded previously)

1) Go to the `Secure S3 File Portal` 
2) Upload a file
3) Verify the availble 'Actions' in the File Portal > Stored Files section.

**Output**
 3) The available actions for the upladed file are: Download and Delete.
 4) The Download and Delete options are clickable.


### File Metadata Correctness


### Error/Degraded Behavior 
When storage is unavailable -> error messaging clarity

#### Scenario ##: Attempt to upload a file without selecting a file


### Negative Scenarios 
Empty file behaivour, unusual filenames, repeated uploads, and browser refresh after actions

### Edge Scenarios

#### Scenario : ASCII characters are supported in objectc's filename 
**Pre-requisite:**
- Secure S3 File Portal initial state (no file has been uploaded previously)

Access the `Secure S3 File Portal` and verify th