
from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get("/health", tags=["Health"])
async def health_check():

    return {
        "success": True,
        "message": "Application is running",
        "application": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
    }
