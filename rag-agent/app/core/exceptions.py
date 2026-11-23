import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class AppException(Exception):
    """
    Base exception for application-level errors.
    """

    def __init__(self,message: str,status_code: int = 500):
        self.message = message
        self.status_code = status_code

        super().__init__(message)


class ResourceNotFoundException(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)


class ExternalServiceException(AppException):
    def __init__(self, message: str = "External service unavailable"):
        super().__init__(message, status_code=503)


async def app_exception_handler(request: Request,exc: AppException,) -> JSONResponse:

    logger.warning("Application exception: %s | Path: %s",exc.message,request.url.path,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "message": exc.message,
            },
        },
    )


async def general_exception_handler(request: Request,exc: Exception,) -> JSONResponse:

    logger.exception("Unhandled exception | Path: %s",request.url.path,)

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "message": "An internal server error occurred.",
            },
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register centralized exception handlers.
    """

    app.add_exception_handler(
        AppException,
        app_exception_handler,
    )

    app.add_exception_handler(
        Exception,
        general_exception_handler,
    )
