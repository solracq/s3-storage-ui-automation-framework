from __future__ import annotations

from datetime import UTC, datetime
from io import BytesIO
from pathlib import PurePosixPath
from uuid import uuid4

from fastapi import UploadFile
from minio import Minio
from minio.error import S3Error

from app.storage_portal.models.storage import StoredFile
from app.storage_portal.settings import Settings


class StorageService:
    """
    Encapsulates all MinIO/S3 object operations for the portal UI.
    This storage service is the app's storage adapter. It hides MinIO details from the UI layer
    and gives the rest of the app a clean Python API.
    """
    def __init__(self, settings: Settings) -> None:
        """
        Create a storage service using the app's configured MinIO settings.
        """
        self._settings = settings
        self._client = Minio(
            endpoint=settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=settings.minio_secure,
        )

    @property
    def bucket_name(self) -> str:
        """
        Return the bucket name used by the portal.
        """
        return self._settings.minio_bucket_name

    def ensure_bucket(self) -> None:
        """
        Create the configured bucket if it does not already exist.
        """
        if not self._client.bucket_exists(self.bucket_name):
            self._client.make_bucket(self.bucket_name)

    def check_connection(self) -> tuple[bool, str | None]:
        """
        Validate storage availability and return a success flag plus optional error.
        """
        try:
            self.ensure_bucket()
            return True, None
        except Exception as exc:  # pragma: no cover - exercised manually in Phase 1
            return False, self._format_error(exc)

    def list_files(self) -> list[StoredFile]:
        """
        Return stored files sorted from newest to oldest.
        """
        self.ensure_bucket()

        items: list[StoredFile] = []
        for object_item in self._client.list_objects(self.bucket_name, recursive=True):
            stat = self._client.stat_object(self.bucket_name, object_item.object_name)
            items.append(self._build_stored_file(object_item.object_name, stat))

        return sorted(
            items,
            key=lambda item: item.uploaded_at or datetime.min.replace(tzinfo=UTC),
            reverse=True,
        )

    def upload_file(self, file: UploadFile, uploaded_by: str) -> StoredFile:
        """
        Upload a file object and return the saved file metadata.
        """
        self.ensure_bucket()

        if not file.filename:
            raise ValueError("Please choose a file before uploading.")

        file_name = PurePosixPath(file.filename).name
        file_bytes = file.file.read()
        if not file_bytes:
            raise ValueError("Please upload a non-empty file.")

        object_key = self._build_object_key(file_name)
        content_type = file.content_type or "application/octet-stream"

        self._client.put_object(
            bucket_name=self.bucket_name,
            object_name=object_key,
            data=BytesIO(file_bytes),
            length=len(file_bytes),
            content_type=content_type,
            metadata={
                "uploaded-by": uploaded_by,
                "original-filename": file_name,
            },
        )

        stat = self._client.stat_object(self.bucket_name, object_key)
        return self._build_stored_file(object_key, stat)

    def download_file(self, object_key: str) -> tuple[bytes, StoredFile]:
        """
        Download a stored object and return its bytes plus metadata.
        """
        self.ensure_bucket()

        stat = self._client.stat_object(self.bucket_name, object_key)
        response = self._client.get_object(self.bucket_name, object_key)
        try:
            file_bytes = response.read()
        finally:
            response.close()
            response.release_conn()

        return file_bytes, self._build_stored_file(object_key, stat)

    def delete_file(self, object_key: str) -> None:
        """
        Delete a stored object by key.
        """
        self.ensure_bucket()
        self._client.remove_object(self.bucket_name, object_key)

    def _build_object_key(self, filename: str) -> str:
        """
        Generate a unique object key while preserving the original filename.
        """
        timestamp = datetime.now(tz=UTC).strftime("%Y%m%dT%H%M%SZ")
        unique_suffix = uuid4().hex[:8]
        return f"portal-uploads/{timestamp}-{unique_suffix}-{filename}"

    def _build_stored_file(self, object_key: str, stat) -> StoredFile:
        """
        Map MinIO object metadata into the app's StoredFile model.
        """
        metadata = {key.lower(): value for key, value in (stat.metadata or {}).items()}

        return StoredFile(
            filename=metadata.get("x-amz-meta-original-filename", PurePosixPath(object_key).name),
            object_key=object_key,
            uploaded_by=metadata.get("x-amz-meta-uploaded-by", "unknown"),
            content_type=stat.content_type or "application/octet-stream",
            uploaded_at=stat.last_modified,
            size_bytes=stat.size,
        )

    def _format_error(self, exc: Exception) -> str:
        """
        Normalize storage exceptions into UI-friendly error text.
        """
        if isinstance(exc, S3Error):
            return f"{exc.code}: {exc.message}"

        message = str(exc).strip()
        return message or exc.__class__.__name__
