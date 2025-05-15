from typing import Dict
import boto3
from botocore.exceptions import ClientError
from app.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION

class AwsResponse:
    """Response model for AWS operations"""
    def __init__(self, success: bool, data: Dict = None, error: str = None):
        self.success = success
        self.data = data
        self.error = error

class AwsService:
    """Service for handling AWS operations"""
    def __init__(self):
        """Initialize AWS clients"""
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )

    def upload_resume(self, file_path: str, bucket: str, key: str) -> AwsResponse:
        """Upload a resume file to S3"""
        try:
            self.s3.upload_file(file_path, bucket, key)
            return AwsResponse(
                success=True,
                data={"bucket": bucket, "key": key}
            )
        except ClientError as e:
            return AwsResponse(
                success=False,
                error=str(e)
            )

    def get_resume_url(self, bucket: str, key: str, expires_in: int = 3600) -> AwsResponse:
        """Generate a pre-signed URL for a resume file"""
        try:
            url = self.s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket, 'Key': key},
                ExpiresIn=expires_in
            )
            return AwsResponse(
                success=True,
                data={"url": url}
            )
        except ClientError as e:
            return AwsResponse(
                success=False,
                error=str(e)
            )
