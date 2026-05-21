from sqlalchemy.orm import Session, joinedload
from app.repository.base import BaseRepository
from app.models.patient import Patient

class PatientRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(model_class=Patient, db=db)

    def get_by_mrn(self, mrn: str):
        return (
            self.db.query(Patient)
            .options(joinedload(Patient.person))
            .filter(Patient.mrn == mrn)
            .first()
        )
    
    def get_by_id(self, id: str):
        patient = (
            self.db.query(Patient)
            .options(
                joinedload(Patient.person),
                joinedload(Patient.visits),
            )
            .filter(Patient.id == id)
            .first()
        )

        return patient