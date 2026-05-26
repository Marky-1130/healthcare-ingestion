from fastapi import APIRouter

from app.core.database import get_async_db
from app.schemas.ingest import VisitIngestSchema
from app.services.ingestion_service import IngestionService


router = APIRouter(prefix="", tags=["Ingest"])

@router.post("/ingest")
async def ingest_patients(payload: list[VisitIngestSchema]):
    service = IngestionService()
    return await service.ingest(payload)