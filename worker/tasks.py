from pathlib import Path
import csv
from app.core.database import SessionLocal
from app.services.s3_service import S3Service
from app.models import Patient, Person, Visit
from app.repository.patient import PatientRepository
from app.repository.person import PersonRepository
from app.repository.visit import VisitRepository
from worker.celery_app import celery

@celery.task(name="worker.tasks.process_csv_task")
def process_csv_task(object_name: str):
    temp_file = f"/tmp/{object_name}"
    s3_service = S3Service()
    s3_service.download_file(object_name, temp_file)

    db = SessionLocal()
    patient_repo = PatientRepository(db)
    person_repo = PersonRepository(db)
    visit_repo = VisitRepository(db)

    try:
        with open(temp_file, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                existing_patient = patient_repo.get_by_mrn(row["mrn"])
                
                if existing_patient:
                    print("Existing Patient")
                    existing_patient.person.first_name = row["first_name"]
                    existing_patient.person.last_name = row["last_name"]
                    existing_patient.person.birth_date = row["birth_date"]
                    patient_id = existing_patient.id

                else:
                    patient = Patient(mrn=row["mrn"])
                    patient_repo.add(patient)

                    person = Person(
                        id=patient.id,
                        first_name=row["first_name"],
                        last_name=row["last_name"],
                        birth_date=row["birth_date"],
                    )
                    person_repo.add(person)
                    patient_id = patient.id

                # Handle visit
                existing_visit = visit_repo.get_by_account_number(
                    row["visit_account_number"]
                )
                if existing_visit:
                    continue

                visit = Visit(
                    visit_account_number=row["visit_account_number"],
                    patient_id=patient_id,
                    visit_date=row["visit_date"],
                    reason=row["reason"],
                )
                visit_repo.add(visit)
                db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()
        if Path(temp_file).exists():
            Path(temp_file).unlink()