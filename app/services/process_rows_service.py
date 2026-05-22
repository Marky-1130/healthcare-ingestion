from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.models import Patient, Person, Visit
from app.repository.patient import PatientRepository
from app.repository.person import PersonRepository
from app.repository.visit import VisitRepository

from app.exceptions.base import DatabaseException, ValidationException

logger = get_logger(__name__)

class ProcessRowsService:
    def __init__(self, db: Session):
        self.db = db
        self.patient_repo = PatientRepository(db)
        self.person_repo = PersonRepository(db)
        self.visit_repo = VisitRepository(db)

    def process_csv_rows(self, rows: list):
        if not rows:
            raise ValidationException(message=f"Rows cannot be empty")

        for row in rows:
            try:
                self._process_row(row)
            
            except SQLAlchemyError as e:
                self.db.rollback()
                raise DatabaseException(message=f"Database error occurred: {e}") from e 
            
        self.db.commit()

    def _process_row(self, row: dict) -> None:
        patient_id = self._upsert_patient(row)
        self._create_visit(row, patient_id)

    def _upsert_patient(self, row: dict) -> int:
        existing_patient = self.patient_repo.get_by_mrn(row["mrn"])

        if existing_patient:
            logger.info(f"Existing Patient: {existing_patient.mrn} - Updating details if applicable.")
            existing_patient.person.first_name = row["first_name"]
            existing_patient.person.last_name = row["last_name"]
            existing_patient.person.birth_date = row["birth_date"]

            return existing_patient.id

        patient = Patient(mrn=row["mrn"])
        self.patient_repo.add(patient)

        self.db.flush()

        person = Person(
            id=patient.id,
            first_name=row["first_name"],
            last_name=row["last_name"],
            birth_date=row["birth_date"]
        )

        self.person_repo.add(person)
        logger.info(f"Adding patient details: {patient.mrn}")

        return patient.id

    def _create_visit(self, row: dict, patient_id: int,) -> None:
        existing_visit = (
            self.visit_repo.get_by_account_number(row["visit_account_number"])
        )

        if existing_visit:
            logger.info(f"Existing visit number: {existing_visit.visit_account_number} - Skipping add")
            return

        visit = Visit(
            visit_account_number=row["visit_account_number"],
            patient_id=patient_id,
            visit_date=row["visit_date"],
            reason=row.get("reason")
        )

        logger.info(f"Adding visit details: {visit.visit_account_number}")
        self.visit_repo.add(visit)