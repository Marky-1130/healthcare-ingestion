from temporalio import activity
from app.core.logging import get_logger
from app.core.database import AsyncSessionLocal
from app.services.process_rows_service import ProcessRowsService

logger = get_logger(__name__)

@activity.defn
async def db_insert_activity(rows: list) -> int:
    async with AsyncSessionLocal() as db:
        row_service = ProcessRowsService(db)

        logger.info("Database activities starting..")
        await row_service.process_csv_rows(rows=rows)

        await db.commit()

    return len(rows)