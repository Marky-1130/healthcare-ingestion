import csv
import uuid
from pathlib import Path
from app.schemas.ingest import VisitIngestSchema

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

class CSVService:
    columns = [
        "mrn",
        "first_name",
        "last_name",
        "birth_date",
        "visit_account_number",
        "visit_date",
        "reason",
    ]

    @classmethod
    def generate_csv(cls, records: list[VisitIngestSchema])-> str:
        file_name = f"patient_ingest_{uuid.uuid4()}.csv"
        file_path = UPLOAD_DIR / file_name
        with open(file_path, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.columns)
            writer.writeheader()
            for record in records:
                writer.writerow(record.model_dump())
        
        return str(file_path)