from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy


with workflow.unsafe.imports_passed_through():
    from worker.activities.s3_activities import download_csv_activity
    from worker.activities.csv_activities import parse_csv_activity
    from worker.activities.db_activities import db_insert_activity
    from worker.activities.audit_ingestion_activity import audit_ingestion_activity

@workflow.defn
class PatientIngestionWorkflow:

    @workflow.run
    async def run(self, object_name: str):

        file_path = await workflow.execute_activity(
            download_csv_activity,
            object_name,
            start_to_close_timeout=timedelta(minutes=3),
            retry_policy=RetryPolicy(
                maximum_attempts=3
            )
        )

        rows = await workflow.execute_activity(
            parse_csv_activity,
            file_path,
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=RetryPolicy(
                maximum_attempts=3
            )
        )

        processed_rows = await workflow.execute_activity(
            db_insert_activity,
            rows,
            schedule_to_close_timeout=timedelta(minutes=10),
            retry_policy=RetryPolicy(
                maximum_attempts=3
            )
        )

        await workflow.execute_activity(
            audit_ingestion_activity,
            processed_rows,
            schedule_to_close_timeout=timedelta(minutes=1)
        )

