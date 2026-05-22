from pathlib import Path
from app.schemas.ingest import VisitIngestSchema
from app.services.generate_csv_service import GenerateCSVService
from app.services.s3_service import S3Service
from app.exceptions.base import ValidationException
from app.core.logging import get_logger
from worker.tasks import process_csv_task

logger = get_logger(__name__)

class IngestionService:
    def __init__(self):
        self.s3_service = S3Service()

    def ingest(self, payload: list[VisitIngestSchema]):
        if not payload:
            logger.error("Empty ingestion payload received")

            raise ValidationException(
                message="Payload cannot be empty.",
                status_code=400
            )

        logger.info(f"Starting ingestion for {len(payload)} records")

        csv_path = GenerateCSVService.generate_csv(payload)
        file_name = Path(csv_path).name
        self.s3_service.upload_file(csv_path, file_name)
        process_csv_task.delay(file_name)

        logger.info(f"CSV uploaded and task queued: {file_name}")

        return {
            "message": "Ingestion started",
            "file": file_name,
        }