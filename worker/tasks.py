from pathlib import Path
from app.core.database import SessionLocal
from app.services.s3_service import S3Service
from app.services.import_csv_service import ImportCSVService
from worker.celery_app import celery
from app.core.logging import get_logger

logger = get_logger(__name__)

@celery.task(name="worker.tasks.process_csv_task")
def process_csv_task(object_name: str):
    temp_file = f"/tmp/{object_name}"
    logger.info(f"Starting CSV processing for file: {object_name}")

    db = SessionLocal()

    try:
        s3_service = S3Service()
        s3_service.download_file(object_name, temp_file)
        import_csv_service = ImportCSVService(db)
        import_csv_service.process_file(temp_file)

    finally:
        db.close()
        if Path(temp_file).exists():
            Path(temp_file).unlink()