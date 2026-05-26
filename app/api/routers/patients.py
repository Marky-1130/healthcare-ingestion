from fastapi import APIRouter
from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_db
from app.schemas.ingest import VisitIngestSchema
from app.schemas.patient import PatientResponse, PaginatedResponse
from app.services.ingestion_service import IngestionService
from app.services.patient_service import PatientService

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.get("", response_model=PaginatedResponse[PatientResponse])
async def get_patients(
        db: AsyncSession = Depends(get_async_db),
        page: int = Query(default=1, ge=1),
        size: int = Query(default=10, ge=1, le=100),
        mrn: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ):
    
    service = PatientService(db)
    return await service.get_patients(page=page, size=size, mrn=mrn, first_name=first_name, last_name=last_name)

@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(
        patient_id: str,
        db: AsyncSession = Depends(get_async_db),
    ):
    service = PatientService(db)
    return await service.get_patient_by_id(patient_id)