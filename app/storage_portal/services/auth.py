"""
Authentication service for local demo users.
"""

from __future__ import annotations

import json

from app.storage_portal.models.auth import DemoUser
from app.storage_portal.settings import Settings


class AuthService:
    """
    Manage demo user data and authentication for the portal.
    """

    DEFAULT_USERS = (
        DemoUser(
            username="admin",
            password="admin123",
            role="admin",
            display_name="Portal Administrator",
        ),
        DemoUser(
            username="viewer",
            password="viewer123",
            role="viewer",
            display_name="Read-Only Viewer",
        ),
    )

    def __init__(self, settings: Settings) -> None:
        """
        Initialize the auth service and ensure the demo user seed file exists.
        """
        self._settings = settings
        self.seed_default_users()

    def seed_default_users(self, overwrite: bool = False) -> list[DemoUser]:
        """
        Create the demo user seed file if needed and optionally overwrite it.
        """
        self._settings.demo_users_file.parent.mkdir(parents=True, exist_ok=True)

        if self._settings.demo_users_file.exists() and not overwrite:
            return self.list_users()

        payload = [
            {
                "username": user.username,
                "password": user.password,
                "role": user.role,
                "display_name": user.display_name,
            }
            for user in self.DEFAULT_USERS
        ]
        self._settings.demo_users_file.write_text(
            json.dumps(payload, indent=2),
            encoding="utf-8",
        )
        return list(self.DEFAULT_USERS)

    def list_users(self) -> list[DemoUser]:
        """
        Return every configured demo user.
        """
        if not self._settings.demo_users_file.exists():
            return self.seed_default_users()

        payload = json.loads(
            self._settings.demo_users_file.read_text(encoding="utf-8")
        )
        return [DemoUser(**item) for item in payload]

    def get_user(self, username: str) -> DemoUser | None:
        """
        Return one user by username if the user exists.
        """
        normalized = username.strip().lower()
        for user in self.list_users():
            if user.username == normalized:
                return user
        return None

    def authenticate(self, username: str, password: str) -> DemoUser | None:
        """
        Validate a username and password against the demo user store.
        """
        user = self.get_user(username)
        if user is None or user.password != password:
            return None
        return user
