import os
from typing import Optional
from pydantic_settings import BaseSettings

class AWSSettings(BaseSettings):
    """AWS Configuration Settings"""
    
    # AWS Credentials
    AWS_ACCESS_KEY_ID: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    
    # S3 Settings
    S3_BUCKET_NAME: Optional[str] = os.getenv("S3_BUCKET_NAME")
    S3_ENDPOINT_URL: Optional[str] = os.getenv("S3_ENDPOINT_URL")
    
    # DynamoDB Settings
    DYNAMODB_TABLE_NAME: Optional[str] = os.getenv("DYNAMODB_TABLE_NAME")
    DYNAMODB_ENDPOINT_URL: Optional[str] = os.getenv("DYNAMODB_ENDPOINT_URL")
    
    # SES Settings (for email)
    SES_REGION: Optional[str] = os.getenv("SES_REGION")
    SES_SENDER_EMAIL: Optional[str] = os.getenv("SES_SENDER_EMAIL")
    
    # CloudWatch Settings
    CLOUDWATCH_LOG_GROUP: Optional[str] = os.getenv("CLOUDWATCH_LOG_GROUP")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create a global instance of the settings
aws_settings = AWSSettings()

def get_aws_settings() -> AWSSettings:
    """Get AWS settings instance"""
    return aws_settings 