from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class StoredFile:
    """
    Represents a file stored in MinIO along with UI-friendly metadata.
    """
    filename: str
    object_key: str
    uploaded_by: str
    content_type: str
    uploaded_at: datetime | None
    size_bytes: int

    @property
    def size_label(self) -> str:
        """
        Return the file size formatted in a human-readable unit.
        This property converts size_bytes into something like 42 B, 3.1 KB, or 1.4 MB
        """
        units = ["B", "KB", "MB", "GB"]
        size = float(self.size_bytes)
        unit_index = 0

        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1

        if unit_index == 0:
            return f"{int(size)} {units[unit_index]}"

        return f"{size:.1f} {units[unit_index]}"
