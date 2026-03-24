import pytest
import boto3
from botocore.exceptions import ClientError

def test_bucket_exists(s3_client):
    """Verify that the S3 bucket defined in Troposphere was created."""
    bucket_name = "regional-map-2024-website"
    try:
        response = s3_client.head_bucket(Bucket=bucket_name)
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200
    except ClientError:
        pytest.fail(f"Bucket {bucket_name} was not found in LocalStack.")

def test_iam_role_exists(iam_client):
    """Verify the WebServerRole exists and has the correct AssumeRolePolicy."""
    role_name = "iam-WebServerRole"
    try:
        response = iam_client.get_role(RoleName=role_name)
        assert response["Role"]["RoleName"] == role_name
        
        policy = response["Role"]["AssumeRolePolicyDocument"]
        statement = policy["Statement"][0]

        actual_service = statement["Principal"]["Service"]
        services = actual_service if isinstance(actual_service, list) else [actual_service]
        assert "ec2.amazonaws.com" in services

        actual_action = statement["Action"]
        actions = actual_action if isinstance(actual_action, list) else [actual_action]
        assert "sts:AssumeRole" in actions
    except ClientError:
        pytest.fail(f"Role {role_name} was not found.")

def test_s3_security_config(s3_client):
    """ELITE: Verify Security Guardrails (Public Access Block)."""
    bucket_name = "regional-map-2024-website"
    try:
        response = s3_client.get_public_access_block(Bucket=bucket_name)
        config = response['PublicAccessBlockConfiguration']
        
        assert config['BlockPublicAcls'] is True
        assert config['IgnorePublicAcls'] is True
    except ClientError:
        pytest.fail(f"S3 Security Check failed! {bucket_name} is missing Public Access Block.")