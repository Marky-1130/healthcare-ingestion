from pathlib import Path
from app.schemas.ingest import VisitIngestSchema
from app.services.generate_csv_service import GenerateCSVService
from app.services.s3_service import S3Service
from app.exceptions.base import ValidationException
from app.core.logging import get_logger
from app.core.temporal import get_temporal_client
from worker.workflows.patient_ingestion_workflow import PatientIngestionWorkflow

logger = get_logger(__name__)

class IngestionService:
    def __init__(self):
        self.s3_service = S3Service()

    async def ingest(self, payload: list[VisitIngestSchema]):
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

        client = await get_temporal_client()
        await client.start_workflow(
            PatientIngestionWorkflow.run,
            file_name,
            id=f"patient-ingestion-{file_name}",
            task_queue="patient-ingestion",
        )

        logger.info(f"CSV uploaded and task queued: {file_name}")

        return {
            "message": "Ingestion started",
            "file": file_name,
        }