import pytest
import boto3
import os

# Centralized configuration
LOCALSTACK_ENDPOINT = os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566")
REGION = "us-east-1"

@pytest.fixture(scope="session")
def stack_name():
    """Returns the stack name from environment or a default."""
    return os.getenv("STACK_NAME", "STK")

@pytest.fixture(scope="session")
def aws_config():
    """Standardized credentials for LocalStack."""
    return {
        "endpoint_url": LOCALSTACK_ENDPOINT,
        "region_name": REGION,
        "aws_access_key_id": "test",
        "aws_secret_access_key": "test",
    }

@pytest.fixture(scope="session")
def s3_client(aws_config):
    """Fixture for S3 client pointing to LocalStack."""
    return boto3.client("s3", **aws_config)

@pytest.fixture(scope="session")
def iam_client(aws_config):
    """Fixture for IAM client pointing to LocalStack."""
    return boto3.client("iam", **aws_config)
