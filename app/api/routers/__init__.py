from fastapi import APIRouter
from .patients import router as patients_router
from .ingest import router as ingest_router

router = APIRouter(prefix="/api/v1")

router.include_router(patients_router)
router.include_router(ingest_router)