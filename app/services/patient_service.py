from sqlalchemy.orm import Session
from app.repository.patient import PatientRepository

class PatientService:
    def __init__(self, db: Session):
        self.repo = PatientRepository(db)

    def get_patient_by_id(self, id: str):
        patient = self.repo.get_by_id(id)

        return patient
    
    def get_patients(
        self,
        skip: int = 0,
        limit: int = 10,
        mrn: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ):
        return self.repo.get_patients(skip, limit, mrn, first_name, last_name)