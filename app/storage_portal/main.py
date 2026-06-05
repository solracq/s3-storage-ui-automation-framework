"""
Application entry point for the Secure S3 File Portal.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import Response
from starlette.middleware.sessions import SessionMiddleware

from app.storage_portal.routes.ui import router as ui_router
from app.storage_portal.services.audit import AuditService
from app.storage_portal.services.auth import AuthService
from app.storage_portal.services.storage import StorageService
from app.storage_portal.settings import get_settings

APP_SETTINGS = get_settings()
BASE_DIR = Path(__file__).resolve().parent
STYLESHEET_PATH = BASE_DIR / "static" / "styles.css"
STYLESHEET_CONTENT = STYLESHEET_PATH.read_text(encoding="utf-8")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initialize shared services when the FastAPI app starts.
    """
    app.state.settings = APP_SETTINGS
    app.state.storage_service = StorageService(APP_SETTINGS)
    app.state.auth_service = AuthService(APP_SETTINGS)
    app.state.audit_service = AuditService(APP_SETTINGS)

    try:
        app.state.storage_service.ensure_bucket()
    except Exception:
        # The dashboard and health endpoint surface storage readiness in the UI.
        pass

    yield


app = FastAPI(title="Secure S3 File Portal", lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=APP_SETTINGS.session_secret_key)
app.include_router(ui_router)


@app.get("/static/styles.css", name="portal_stylesheet")
async def portal_stylesheet() -> Response:
    """
    Serve the portal stylesheet without relying on StaticFiles.
    """
    return Response(content=STYLESHEET_CONTENT, media_type="text/css")


@app.get("/health")
async def health(request: Request) -> dict[str, str | bool | None]:
    """
    Return the current application and storage health state.
    """
    storage_ready, storage_error = request.app.state.storage_service.check_connection()
    return {
        "status": "ok" if storage_ready else "degraded",
        "storage_ready": storage_ready,
        "bucket": request.app.state.settings.minio_bucket_name,
        "storage_error": storage_error,
    }
