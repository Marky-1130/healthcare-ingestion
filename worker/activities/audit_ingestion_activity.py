from temporalio import activity
from app.core.logging import get_logger

logger = get_logger(__name__)

@activity.defn
async def audit_ingestion_activity(total_rows: int):
    logger.info(f"Ingestion completed for {total_rows} rows")