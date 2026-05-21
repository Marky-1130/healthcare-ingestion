from fastapi import APIRouter
from .patients import router as patients_router

router = APIRouter(prefix="/api/v1")

router.include_router(patients_router)