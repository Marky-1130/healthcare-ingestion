from fastapi import FastAPI
from app.api.routers import router
from app.core.config import settings
from app.core.database import Base
from app.core.database import engine

from app.services.s3_service import S3Service

#Create the tables
import app.models
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)

app.include_router(router)

@app.get("/")
def healthcheck():
    s3 = S3Service()
    s3.check_connection()
    return {
        "status": "healthy"
    }