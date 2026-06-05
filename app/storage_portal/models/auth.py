"""
Authentication and authorization models for the portal.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DemoUser:
    """
    Represents one local demo user for the portal.
    """

    username: str
    password: str
    role: str
    display_name: str

    @property
    def is_admin(self) -> bool:
        """
        Return whether the user has administrator privileges.
        """
        return self.role == "admin"

    @property
    def can_upload(self) -> bool:
        """
        Return whether the user can upload files.
        """
        return self.is_admin

    @property
    def can_delete(self) -> bool:
        """
        Return whether the user can delete files.
        """
        return self.is_admin

    @property
    def can_view_audit_logs(self) -> bool:
        """
        Return whether the user can view the audit log page.
        """
        return self.is_admin
