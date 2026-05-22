from fastapi import FastAPI
from app.api.routers import router
from app.core.config import settings
from app.core.database import Base
from app.core.database import engine
from app.services.s3_service import S3Service
from app.core.logging import get_logger

app = FastAPI(title=settings.APP_NAME)

app.include_router(router)

logger = get_logger(__name__)

@app.get("/")
def healthcheck():
    logger.info(f"Executing Heath Check")
    return {
        "status": "healthy"
    }