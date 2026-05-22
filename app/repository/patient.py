from typing import List
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
    
    def get_patients(
            self,
            skip: int = 0,
            limit: int = 10,
            mrn: str | None = None,
            first_name: str | None = None,
            last_name: str | None = None,
        ) -> List[Patient]:
        
        query = self.db.query(Patient).options(
            joinedload(Patient.person),
            joinedload(Patient.visits),
        )
        if mrn:
            query = query.filter(Patient.mrn == mrn)
        if first_name:
            query = query.filter(Patient.person.has(first_name=first_name))
        if last_name:
            query = query.filter(Patient.person.has(last_name=last_name))

        total = query.count()
        items = query.offset(skip).limit(limit).all()

        return items, total