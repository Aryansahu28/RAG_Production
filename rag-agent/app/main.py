from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import get_logger, setup_logging

setup_logging()

logger = get_logger(__name__)

def create_application() -> FastAPI:

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Production-oriented RAG Agent",
         debug=settings.debug,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        openapi_url="/openapi.json" if settings.debug else None,
    )

    register_exception_handlers(app)

    app.include_router(
        api_router,
        prefix=settings.api_v1_prefix,

    )

    logger.info("%s application initialized",settings.app_name)

    return app 

app = create_application()
