import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

class RequestIDFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, "request_id"):
            record.request_id = "system"
        
        return True

LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | "
    "%(request_id)s | %(name)s | %(message)s"
)

formatter = logging.Formatter(LOG_FORMAT)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
console_handler.addFilter(RequestIDFilter())

file_handler = RotatingFileHandler(
    filename="logs/app.log",
    maxBytes=10 * 1024 * 1024,
    backupCount=5,
)

file_handler.setFormatter(formatter)
file_handler.addFilter(RequestIDFilter())

logging.basicConfig(
    level=logging.INFO,
    handlers=[console_handler, file_handler],
)

def get_logger(name: str):
    return logging.getLogger(name)