"""
Reset portal storage and local runtime state for repeatable testing.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.storage_portal.services.audit import AuditService
from app.storage_portal.services.auth import AuthService
from app.storage_portal.services.storage import StorageService
from app.storage_portal.settings import get_settings


def main() -> None:
    """
    Clear stored files, reset audit logs, and reseed demo users.
    """
    settings = get_settings()
    storage_service = StorageService(settings)
    auth_service = AuthService(settings)
    audit_service = AuditService(settings)

    deleted_files = storage_service.delete_all_files()
    audit_service.clear_entries()
    auth_service.seed_default_users(overwrite=True)

    print("Portal environment reset complete.")
    print(f"Deleted objects: {deleted_files}")
    print(f"Users file: {settings.demo_users_file}")
    print(f"Audit log file: {settings.audit_log_file}")


if __name__ == "__main__":
    main()
