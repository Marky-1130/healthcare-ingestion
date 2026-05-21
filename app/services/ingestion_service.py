from pathlib import Path
from app.schemas.ingest import VisitIngestSchema
from app.services.csv_service import CSVService
from app.services.s3_service import S3Service
from worker.tasks import process_csv_task

class IngestionService:
    def __init__(self):
        pass
        self.s3_service = S3Service()

    def ingest(self, payload: list[VisitIngestSchema]):
        csv_path = CSVService.generate_csv(payload)
        file_name = Path(csv_path).name
        self.s3_service.upload_file(csv_path, file_name)
        process_csv_task.delay(file_name)

        return {
            "message": "Ingestion started",
            "file": file_name,
        }