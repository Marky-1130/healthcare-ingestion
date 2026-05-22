from math import ceil
from sqlalchemy.orm import Session
from app.repository.patient import PatientRepository
from app.exceptions.base import RecordNotFound, DatabaseException
from sqlalchemy.exc import SQLAlchemyError

class PatientService:
    def __init__(self, db: Session):
        self.repo = PatientRepository(db)

    def get_patient_by_id(self, id: str):
        try:
            patient = self.repo.get_by_id(id)

            if not patient:
                raise RecordNotFound(
                    message=f"Record not found for id: {id}",
                    status_code=404
                )
            
            return patient
        
        except SQLAlchemyError as e:
                raise DatabaseException(
                    message="Database connection error",
                    status_code=503
                )

    def get_patients(
        self,
        page: int = 1,
        size: int = 10,
        mrn: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ):
        try:
            skip = (page - 1) * size

            items, total = self.repo.get_patients(
                skip=skip,
                limit=size,
                mrn=mrn,
                first_name=first_name,
                last_name=last_name,
            )

            pages = ceil(total / size) if size else 1

            return {
                "data": items,
                "page": page,
                "size": size,
                "total": total,
                "pages": pages
            }

        except SQLAlchemyError:
            raise DatabaseException(
                message="Database error while fetching patients",
                status_code=503,
            )