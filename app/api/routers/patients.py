from fastapi import APIRouter
from fastapi import Depends, Query
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.models.patient import Patient
from app.schemas.ingest import VisitIngestSchema
from app.schemas.patient import PatientResponse
from app.services.ingestion_service import IngestionService

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("/ingest")
def ingest_patients(payload: list[VisitIngestSchema]):
    service = IngestionService()
    return service.ingest(payload)

@router.get("", response_model=list[PatientResponse])
def get_patients(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = Query(default=10, le=100),
        mrn: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ):
    
    pass

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(
        patient_id: str,
        db: Session = Depends(get_db),
    ):

    pass