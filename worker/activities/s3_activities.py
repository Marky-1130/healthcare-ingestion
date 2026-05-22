from temporalio import activity
from app.core.logging import get_logger
from app.services.s3_service import S3Service

logger = get_logger(__name__)

@activity.defn
async def download_csv_activity(object_name: str) -> str:
    s3_service = S3Service()
    temp_file = f"/tmp/{object_name}"

    logger.info("Temporal task starting..")
    s3_service.download_file(object_name, temp_file)

    return temp_file