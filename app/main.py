from fastapi import FastAPI
from app.api.routers import router
from app.core.config import settings
from app.services.s3_service import S3Service
from app.core.logging import get_logger
from sqlalchemy.exc import SQLAlchemyError
from fastapi.exceptions import RequestValidationError

from app.exceptions.base import AppException
from app.exceptions.handlers import (
    app_exception_handler,
    generic_exception_handler,
    sqlalchemy_exception_handler,
    validation_exception_handler
)

app = FastAPI(title=settings.APP_NAME)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(router)
logger = get_logger(__name__)

@app.get("/")
def healthcheck():
    logger.info(f"Executing Heath Check")
    return {
        "status": "healthy"
    }