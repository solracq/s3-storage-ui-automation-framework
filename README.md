# s3-storage-ui-automation-framework

A small, security-themed web UI built with FastAPI and Jinja2 templates, backed by MinIO/S3-compatible storage. Including a test automation framework for the UI using Selenium WebDriver with Python, Pytest, and the Page Object Model design pattern

This “Secure S3 File Portal” will contain the following functionality:
* User authentication
* Role-based behavior
* File workflows
* Audit logging
* UI testability

# Initial Folder Structure
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
