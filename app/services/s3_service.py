import boto3
import botocore
from app.core.config import settings

class S3Service:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.AWS_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )

    #TODO: For improvement
    def check_connection(self):
        try:
            self.client.list_buckets()
            print("Connection to S3 established.")
        except botocore.exceptions.EndpointConnectionError:
            print("LocalStack is not reachable")
        except botocore.exceptions.ClientError as e:
            print("AWS operation failed:", e) 

    def upload_file(self, file_path: str, object_name: str):
        self.client.upload_file(
            file_path,
            settings.S3_BUCKET,
            object_name,
        )
        
    def download_file(self, object_name: str, target_path: str):
        self.client.download_file(
            settings.S3_BUCKET,
            object_name,
            target_path,
        )