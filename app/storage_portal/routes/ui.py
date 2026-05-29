from __future__ import annotations

from pathlib import Path
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, File, Form, Query, Request, UploadFile, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from app.storage_portal.services.storage import StorageService

router = APIRouter()
templates = Jinja2Templates(
    directory=str(Path(__file__).resolve().parent.parent / "templates")
)


def get_storage_service(request: Request) -> StorageService:
    """
    Return the shared storage service instance from the FastAPI app state.
    """
    return request.app.state.storage_service


@router.get("/", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    message: str | None = Query(default=None),
    message_type: str = Query(default="info"),
    storage_service: StorageService = Depends(get_storage_service),
) -> HTMLResponse:
    """
    Render the main dashboard with storage status, upload controls, and file list.
    """
    files = []
    storage_ready, storage_error = storage_service.check_connection()

    if storage_ready:
        try:
            files = storage_service.list_files()
        except Exception as exc:  # pragma: no cover - exercised manually in Phase 1
            storage_ready = False
            storage_error = str(exc)

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "page_title": "Portal Dashboard",
            "message": message,
            "message_type": message_type,
            "files": files,
            "storage_ready": storage_ready,
            "storage_error": storage_error,
            "settings": request.app.state.settings,
        },
    )


@router.post("/files/upload")
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    storage_service: StorageService = Depends(get_storage_service),
) -> RedirectResponse:
    """
    Handle file uploads and redirect back to the dashboard with a flash message.
    """
    try:
        storage_service.upload_file(
            file=file,
            uploaded_by=request.app.state.settings.default_upload_actor,
        )
    except ValueError as exc:
        return _dashboard_redirect(str(exc), "error")
    except Exception as exc:  # pragma: no cover - exercised manually in Phase 1
        return _dashboard_redirect(f"Upload failed: {exc}", "error")
    finally:
        await file.close()

    return _dashboard_redirect("File uploaded successfully.", "success")


@router.get("/files/download")
async def download_file(
    object_key: str = Query(...),
    storage_service: StorageService = Depends(get_storage_service),
) -> Response:
    """
    Download a stored object and return it as a browser attachment response.
    """
    try:
        file_bytes, stored_file = storage_service.download_file(object_key)
    except Exception as exc:  # pragma: no cover - exercised manually in Phase 1
        return _dashboard_redirect(f"Download failed: {exc}", "error")

    safe_filename = stored_file.filename.replace('"', "")
    headers = {"Content-Disposition": f'attachment; filename="{safe_filename}"'}
    return Response(
        content=file_bytes,
        media_type=stored_file.content_type,
        headers=headers,
    )


@router.post("/files/delete")
async def delete_file(
    object_key: str = Form(...),
    storage_service: StorageService = Depends(get_storage_service),
) -> RedirectResponse:
    """
    Delete a stored object and redirect back to the dashboard with status feedback.
    """
    try:
        storage_service.delete_file(object_key)
    except Exception as exc:  # pragma: no cover - exercised manually in Phase 1
        return _dashboard_redirect(f"Delete failed: {exc}", "error")

    return _dashboard_redirect("File deleted successfully.", "success")


def _dashboard_redirect(message: str, message_type: str) -> RedirectResponse:
    """
    Build a redirect back to the dashboard with message query parameters.
    """
    query_string = urlencode({"message": message, "message_type": message_type})
    return RedirectResponse(
        url=f"/?{query_string}",
        status_code=status.HTTP_303_SEE_OTHER,
    )
