from fastapi import APIRouter
from fastapi import Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.ingest import VisitIngestSchema
from app.schemas.patient import PatientResponse, PaginatedResponse
from app.services.ingestion_service import IngestionService
from app.services.patient_service import PatientService

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("/ingest")
def ingest_patients(payload: list[VisitIngestSchema]):
    service = IngestionService()
    return service.ingest(payload)

@router.get("", response_model=PaginatedResponse[PatientResponse])
def get_patients(
        db: Session = Depends(get_db),
        page: int = Query(default=1, ge=1),
        size: int = Query(default=10, ge=1, le=100),
        mrn: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ):
    
    service = PatientService(db)
    return service.get_patients(page=page, size=size, mrn=mrn, first_name=first_name, last_name=last_name)

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(
        patient_id: str,
        db: Session = Depends(get_db),
    ):
    service = PatientService(db)
    return service.get_patient_by_id(patient_id)