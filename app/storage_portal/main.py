"""
Application entry point
Creates the FastAPI app
"""
from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from app.storage_portal.routes.ui import router as ui_router
from app.storage_portal.services.storage import StorageService
from app.storage_portal.settings import get_settings

# Set the base directory (app/storage_portal)
BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function to define the FastAPI's startup/shutdown hook pattern.
    It runs when the app starts and is a good place to initialize shared services.

    Args:
        app (FastAPI): FastAPI app
    """
    settings = get_settings()
    app.state.settings = settings
    app.state.storage_service = StorageService(settings)

    try:
        # check that bucket exists at startup
        app.state.storage_service.ensure_bucket()
    except Exception:
        # The dashboard surfaces storage readiness so local development still starts cleanly.
        pass

    yield

# Create the FastAPI app with a title and the custom lifespan
app = FastAPI(title="Secure S3 File Portal", lifespan=lifespan)
# Mount /static so CSS and future frontend assets are served properly
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
# Register the UI routes from routes/ui.py
app.include_router(ui_router)


@app.get("/health")
async def health(request: Request) -> dict[str, str | bool | None]:
    """
    Defines a small health endpoint

    Args:
        request (Request): fastapi request type

    Returns:
        dict[str, str | bool | None]: return status, storage_ready, bucket and storage_error
    """
    # Check storage connectivity
    storage_ready, storage_error = request.app.state.storage_service.check_connection()
    return {
        "status": "ok" if storage_ready else "degraded",
        "storage_ready": storage_ready,
        "bucket": request.app.state.settings.minio_bucket_name,
        "storage_error": storage_error,
    }
