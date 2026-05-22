import csv
from temporalio import activity
from app.core.logging import get_logger
from app.exceptions.base import CSVServiceException

logger = get_logger(__name__)

@activity.defn
async def parse_csv_activity(file_path: str) -> list[dict]:
    rows = []
    try:
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                rows.append(row)

            
        logger.info(f"Rows to be processed: {len(rows)}")
        return rows
    
    except csv.Error as e:
        logger.error(f"Failed to process CSV file: {e}")
        raise CSVServiceException(message=f"Failed to process CSV file: {e}") from e