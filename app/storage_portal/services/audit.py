"""
Audit logging service for portal activity.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime

from app.storage_portal.models.audit import AuditEntry
from app.storage_portal.settings import Settings


class AuditService:
    """
    Persist and retrieve local portal audit events.
    """

    def __init__(self, settings: Settings) -> None:
        """
        Initialize the audit log file if it does not already exist.
        """
        self._settings = settings
        self._ensure_log_file()

    def list_entries(self) -> list[AuditEntry]:
        """
        Return audit log entries sorted from newest to oldest.
        """
        payload = self._read_entries()
        entries = [AuditEntry.from_dict(item) for item in payload]
        return sorted(entries, key=lambda entry: entry.occurred_at, reverse=True)

    def record_event(
        self,
        event_type: str,
        username: str,
        role: str,
        outcome: str,
        details: str,
    ) -> AuditEntry:
        """
        Append one audit event to the audit log.
        """
        entry = AuditEntry(
            occurred_at=datetime.now(tz=UTC),
            event_type=event_type,
            username=username,
            role=role,
            outcome=outcome,
            details=details,
        )
        payload = self._read_entries()
        payload.append(entry.to_dict())
        self._write_entries(payload)
        return entry

    def clear_entries(self) -> None:
        """
        Remove all persisted audit entries.
        """
        self._write_entries([])

    def _ensure_log_file(self) -> None:
        """
        Create the audit log file and parent directories if needed.
        """
        self._settings.audit_log_file.parent.mkdir(parents=True, exist_ok=True)
        if not self._settings.audit_log_file.exists():
            self._write_entries([])

    def _read_entries(self) -> list[dict[str, str]]:
        """
        Read raw audit entry data from the JSON log file.
        """
        self._ensure_log_file()
        raw_text = self._settings.audit_log_file.read_text(encoding="utf-8").strip()
        if not raw_text:
            return []
        return json.loads(raw_text)

    def _write_entries(self, payload: list[dict[str, str]]) -> None:
        """
        Write raw audit entry data to the JSON log file.
        """
        self._settings.audit_log_file.write_text(
            json.dumps(payload, indent=2),
            encoding="utf-8",
        )
