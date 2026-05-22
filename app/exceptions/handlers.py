from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from app.core.logging import get_logger
from app.exceptions.base import AppException
from fastapi.exceptions import RequestValidationError

logger = get_logger(__name__)

async def app_exception_handler(request: Request, exc: AppException):
    logger.error(
        f"Application exception: {exc.message}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
        }
    )

async def sqlalchemy_exception_handler(
    request: Request,
    exc: SQLAlchemyError,
):
    logger.exception(
        f"Database exception occurred: {str(exc)}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Database operation failed",
        }
    )

async def generic_exception_handler(
    request: Request,
    exc: Exception,
):
    logger.exception(
        f"Unhandled exception occurred: {str(exc)}"
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
    }
)

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error at {request.url}: {str(exc)}")

    # Transform errors for client-friendly format
    errors = [
        {"field": ".".join(str(loc) for loc in err["loc"]), "msg": err["msg"]}
        for err in exc.errors()
    ]

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation failed",
            "errors": errors
        }
    )