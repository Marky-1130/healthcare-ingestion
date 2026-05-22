import boto3
import botocore
import time
from functools import wraps
from app.core.config import settings
from app.core.logging import get_logger
from app.exceptions.base import S3Exception

logger = get_logger(__name__)

class S3ConnectionException(S3Exception):
    #Extended for a more specific exception for S3 connection
    pass

def s3_retry(retries=3, delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except botocore.exceptions.EndpointConnectionError as e:
                    last_exception = e
                    logger.warning(
                        f"Attempt {attempt}: S3 endpoint not reachable. Retrying in {delay}s..."
                    )
                    time.sleep(delay)
                except botocore.exceptions.ClientError as e:
                    logger.error(f"S3 operation failed in {func.__name__}: {e}")
                    raise S3Exception(f"S3 operation failed: {e}") from e
                
            raise S3ConnectionException(
                f"Unable to connect to S3 after {retries} attempts: {last_exception}"
            )
        return wrapper
    return decorator

class S3Service:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.AWS_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )

    @s3_retry()
    def check_connection(self):
        self.client.list_buckets()
        logger.info("Connection to S3 established.") 

    @s3_retry()
    def upload_file(self, file_path: str, object_name: str):
        try:
            self.client.upload_file(file_path, settings.S3_BUCKET, object_name)
            logger.info(f"Uploaded {object_name} to bucket {settings.S3_BUCKET}.")
        except Exception as e:
            raise S3Exception(f"Failed to upload file {object_name}: {e}") from e
    
    @s3_retry()
    def download_file(self, object_name: str, target_path: str):
        try:
            self.client.download_file(settings.S3_BUCKET, object_name, target_path)
            logger.info(f"Downloaded {object_name} from bucket {settings.S3_BUCKET}.")
        except Exception as e:
            raise S3Exception(f"Failed to download file {object_name}: {e}") from e