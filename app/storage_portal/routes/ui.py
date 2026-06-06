from __future__ import annotations

from pathlib import Path
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, Form, Query, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from starlette.datastructures import UploadFile
from starlette.formparsers import MultiPartException

from app.storage_portal.models.auth import DemoUser
from app.storage_portal.services.audit import AuditService
from app.storage_portal.services.auth import AuthService
from app.storage_portal.services.storage import StorageService

router = APIRouter()
templates = Jinja2Templates(
    directory=str(Path(__file__).resolve().parent.parent / "templates")
)


async def get_storage_service(request: Request) -> StorageService:
    """Return the shared storage service instance from the FastAPI app state."""
    return request.app.state.storage_service


async def get_auth_service(request: Request) -> AuthService:
    """Return the shared authentication service from the FastAPI app state."""
    return request.app.state.auth_service


async def get_audit_service(request: Request) -> AuditService:
    """Return the shared audit service from the FastAPI app state."""
    return request.app.state.audit_service


@router.get("/", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    message: str | None = Query(default=None),
    message_type: str = Query(default="info"),
    storage_service: StorageService = Depends(get_storage_service),
    auth_service: AuthService = Depends(get_auth_service),
) -> Response:
    """
    Render the main dashboard for an authenticated user.
    """
    current_user = _get_current_user(request, auth_service)
    if current_user is None:
        return _login_redirect("Please sign in to access the portal.", "info")

    files = []
    storage_ready, storage_error = storage_service.check_connection()

    if storage_ready:
        try:
            files = storage_service.list_files()
        except Exception as exc:  # pragma: no cover - exercised manually
            storage_ready = False
            storage_error = str(exc)

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context=_base_context(
            request=request,
            current_user=current_user,
            page_title="Portal Dashboard",
            message=message,
            message_type=message_type,
            files=files,
            storage_ready=storage_ready,
            storage_error=storage_error,
        ),
    )


@router.get("/login", response_class=HTMLResponse)
async def login_page(
    request: Request,
    message: str | None = Query(default=None),
    message_type: str = Query(default="info"),
    auth_service: AuthService = Depends(get_auth_service),
) -> Response:
    """
    Render the login page for unauthenticated users.
    """
    current_user = _get_current_user(request, auth_service)
    if current_user is not None:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context=_base_context(
            request=request,
            current_user=None,
            page_title="Login",
            message=message,
            message_type=message_type,
        ),
    )


@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    auth_service: AuthService = Depends(get_auth_service),
    audit_service: AuditService = Depends(get_audit_service),
) -> RedirectResponse:
    """
    Authenticate a user and create a portal session.
    """
    user = auth_service.authenticate(username, password)
    normalized_username = username.strip().lower() or "anonymous"
    if user is None:
        audit_service.record_event(
            event_type="login_failure",
            username=normalized_username,
            role="unknown",
            outcome="denied",
            details="Invalid username or password.",
        )
        return _login_redirect("Invalid username or password.", "error")

    request.session.clear()
    request.session["username"] = user.username
    audit_service.record_event(
        event_type="login_success",
        username=user.username,
        role=user.role,
        outcome="success",
        details="User authenticated successfully.",
    )
    return _dashboard_redirect("Login successful.", "success")


@router.post("/logout")
async def logout(request: Request) -> RedirectResponse:
    """Clear the current session and return to the login page."""
    request.session.clear()
    return _login_redirect("Logged out successfully.", "success")


@router.get("/access-denied", response_class=HTMLResponse)
async def access_denied(
    request: Request,
    message: str | None = Query(default=None),
    auth_service: AuthService = Depends(get_auth_service),
) -> HTMLResponse:
    """Render a clear access denied page for unauthorized actions."""
    current_user = _get_current_user(request, auth_service)
    return templates.TemplateResponse(
        request=request,
        name="access_denied.html",
        context=_base_context(
            request=request,
            current_user=current_user,
            page_title="Access Denied",
            access_denied_message=message or "You do not have permission to perform that action.",
        ),
    )


@router.get("/audit-logs", response_class=HTMLResponse)
async def audit_logs(
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
    audit_service: AuditService = Depends(get_audit_service),
) -> Response:
    """Render the audit log page for the admin user."""
    current_user = _get_current_user(request, auth_service)
    if current_user is None:
        return _login_redirect("Please sign in to access the portal.", "info")

    if not current_user.can_view_audit_logs:
        audit_service.record_event(
            event_type="unauthorized_access",
            username=current_user.username,
            role=current_user.role,
            outcome="denied",
            details="Attempted to view audit logs.",
        )
        return _access_denied_redirect("Only the admin user can view audit logs.")

    return templates.TemplateResponse(
        request=request,
        name="audit_log.html",
        context=_base_context(
            request=request,
            current_user=current_user,
            page_title="Audit Log",
            audit_entries=audit_service.list_entries(),
        ),
    )


@router.post("/files/upload")
async def upload_file(
    request: Request,
    storage_service: StorageService = Depends(get_storage_service),
    auth_service: AuthService = Depends(get_auth_service),
    audit_service: AuditService = Depends(get_audit_service),
) -> RedirectResponse:
    """Handle admin-only file uploads and redirect back to the dashboard."""
    current_user = _get_current_user(request, auth_service)
    if current_user is None:
        return _login_redirect("Please sign in to access the portal.", "info")

    if not current_user.can_upload:
        audit_service.record_event(
            event_type="unauthorized_access",
            username=current_user.username,
            role=current_user.role,
            outcome="denied",
            details="Attempted to upload a file.",
        )
        return _access_denied_redirect("Only the admin user can upload files.")

    content_length_header = request.headers.get("content-length", "").strip()
    if content_length_header.isdigit():
        content_length = int(content_length_header)
        if content_length > request.app.state.settings.max_upload_request_size_bytes:
            return _dashboard_redirect(
                "Maximum upload size exceeded. This portal currently supports files up to "
                f"{request.app.state.settings.max_upload_size_label}.",
                "error",
            )

    try:
        form = await request.form()
    except MultiPartException:
        return _dashboard_redirect("Upload failed: invalid multipart form data.", "error")

    file = form.get("file")
    if not isinstance(file, UploadFile):
        return _dashboard_redirect("Please choose a file before uploading.", "error")

    try:
        stored_file = storage_service.upload_file(
            file=file,
            uploaded_by=current_user.username,
        )
        audit_service.record_event(
            event_type="file_upload",
            username=current_user.username,
            role=current_user.role,
            outcome="success",
            details=f"Uploaded {stored_file.filename}.",
        )
    except ValueError as exc:
        return _dashboard_redirect(str(exc), "error")
    except Exception as exc:  # pragma: no cover - exercised manually
        return _dashboard_redirect(f"Upload failed: {exc}", "error")
    finally:
        await file.close()

    return _dashboard_redirect("File uploaded successfully.", "success")


@router.get("/files/download")
async def download_file(
    request: Request,
    object_key: str = Query(...),
    storage_service: StorageService = Depends(get_storage_service),
    auth_service: AuthService = Depends(get_auth_service),
    audit_service: AuditService = Depends(get_audit_service),
) -> Response:
    """Download a stored object for an authenticated user."""
    current_user = _get_current_user(request, auth_service)
    if current_user is None:
        return _login_redirect("Please sign in to access the portal.", "info")

    try:
        file_bytes, stored_file = storage_service.download_file(object_key)
    except Exception as exc:  # pragma: no cover - exercised manually
        return _dashboard_redirect(f"Download failed: {exc}", "error")

    audit_service.record_event(
        event_type="file_download",
        username=current_user.username,
        role=current_user.role,
        outcome="success",
        details=f"Downloaded {stored_file.filename}.",
    )
    safe_filename = stored_file.filename.replace('"', "")
    headers = {"Content-Disposition": f'attachment; filename="{safe_filename}"'}
    return Response(
        content=file_bytes,
        media_type=stored_file.content_type,
        headers=headers,
    )


@router.post("/files/delete")
async def delete_file(
    request: Request,
    object_key: str = Form(...),
    storage_service: StorageService = Depends(get_storage_service),
    auth_service: AuthService = Depends(get_auth_service),
    audit_service: AuditService = Depends(get_audit_service),
) -> RedirectResponse:
    """Handle admin-only delete actions and redirect back to the dashboard."""
    current_user = _get_current_user(request, auth_service)
    if current_user is None:
        return _login_redirect("Please sign in to access the portal.", "info")

    if not current_user.can_delete:
        audit_service.record_event(
            event_type="unauthorized_access",
            username=current_user.username,
            role=current_user.role,
            outcome="denied",
            details="Attempted to delete a file.",
        )
        return _access_denied_redirect("Only the admin user can delete files.")

    try:
        storage_service.delete_file(object_key)
        audit_service.record_event(
            event_type="file_delete",
            username=current_user.username,
            role=current_user.role,
            outcome="success",
            details=f"Deleted object {object_key}.",
        )
    except Exception as exc:  # pragma: no cover - exercised manually
        return _dashboard_redirect(f"Delete failed: {exc}", "error")

    return _dashboard_redirect("File deleted successfully.", "success")


def _get_current_user(request: Request, auth_service: AuthService) -> DemoUser | None:
    """Return the currently authenticated user from the session cookie."""
    username = request.session.get("username")
    if not username:
        return None
    return auth_service.get_user(username)


def _base_context(
    request: Request,
    current_user: DemoUser | None,
    page_title: str,
    **extra: object,
) -> dict[str, object]:
    """Build a shared template context for portal pages."""
    context: dict[str, object] = {
        "settings": request.app.state.settings,
        "current_user": current_user,
        "page_title": page_title,
    }
    context.update(extra)
    return context


def _dashboard_redirect(message: str, message_type: str) -> RedirectResponse:
    """Build a redirect back to the dashboard with message query parameters."""
    query_string = urlencode({"message": message, "message_type": message_type})
    return RedirectResponse(
        url=f"/?{query_string}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


def _login_redirect(message: str, message_type: str) -> RedirectResponse:
    """Build a redirect back to the login page with message query parameters."""
    query_string = urlencode({"message": message, "message_type": message_type})
    return RedirectResponse(
        url=f"/login?{query_string}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


def _access_denied_redirect(message: str) -> RedirectResponse:
    """Build a redirect to the access denied page with a clear message."""
    query_string = urlencode({"message": message})
    return RedirectResponse(
        url=f"/access-denied?{query_string}",
        status_code=status.HTTP_303_SEE_OTHER,
    )
