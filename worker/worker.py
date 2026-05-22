import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from worker.activities.s3_activities import download_csv_activity
from worker.activities.csv_activities import parse_csv_activity
from worker.activities.db_activities import db_insert_activity
from worker.activities.audit_ingestion_activity import audit_ingestion_activity
from worker.workflows.patient_ingestion_workflow import PatientIngestionWorkflow


async def main():
    client = await Client.connect(
        "temporal:7233"
    )

    worker = Worker(
        client,
        task_queue="patient-ingestion",
        workflows=[PatientIngestionWorkflow],
        activities=[
            download_csv_activity,
            parse_csv_activity,
            db_insert_activity,
            audit_ingestion_activity
        ]
    )

    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())