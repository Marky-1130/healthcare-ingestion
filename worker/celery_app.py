from celery import Celery
from app.core.config import settings

celery = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery.conf.task_routes = {
    "worker.tasks.process_csv_task": {"queue": "ingestion"}
}

celery.autodiscover_tasks(['worker.tasks'])