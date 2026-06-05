"""
Audit log models for the portal.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class AuditEntry:
    """
    Represents one audit event captured by the portal.
    """

    occurred_at: datetime
    event_type: str
    username: str
    role: str
    outcome: str
    details: str

    @classmethod
    def from_dict(cls, payload: dict[str, str]) -> "AuditEntry":
        """
        Build an audit entry from persisted JSON data.
        """
        return cls(
            occurred_at=datetime.fromisoformat(payload["occurred_at"]),
            event_type=payload["event_type"],
            username=payload["username"],
            role=payload["role"],
            outcome=payload["outcome"],
            details=payload["details"],
        )

    def to_dict(self) -> dict[str, str]:
        """
        Serialize the audit entry into JSON-safe data.
        """
        return {
            "occurred_at": self.occurred_at.isoformat(),
            "event_type": self.event_type,
            "username": self.username,
            "role": self.role,
            "outcome": self.outcome,
            "details": self.details,
        }
