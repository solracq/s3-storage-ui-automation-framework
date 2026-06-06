"""
Seed local demo users for the Secure S3 File Portal.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.storage_portal.services.audit import AuditService
from app.storage_portal.services.auth import AuthService
from app.storage_portal.settings import get_settings


def main() -> None:
    """
    Write the default demo users and ensure the audit log file exists.
    """
    settings = get_settings()
    auth_service = AuthService(settings)
    audit_service = AuditService(settings)

    users = auth_service.seed_default_users(overwrite=True)
    audit_service.clear_entries()

    print("Seeded demo users:")
    for user in users:
        print(f"- {user.username} / {user.password} ({user.role})")
    print(f"Users file: {settings.demo_users_file}")
    print(f"Audit log reset: {settings.audit_log_file}")


if __name__ == "__main__":
    main()
