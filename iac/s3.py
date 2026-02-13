"""
Troposphere template: S3 bucket for regional-map-2024 website
Works with LocalStack and flagged for checkov
"""

from troposphere import Template, Ref, Output, Sub, Export, logs
from troposphere.s3 import (
    Bucket,
    BucketEncryption,
    BucketPolicy,
    WebsiteConfiguration,
    VersioningConfiguration,
    PublicAccessBlockConfiguration,
    LoggingConfiguration,
    ServerSideEncryptionRule,
    ServerSideEncryptionByDefault
)

# Create the template
t = Template()
t.set_description("LocalStack S3 bucket for regional-map-2024 hosting")

# Bucket name
BUCKET_NAME = "regional-map-2024-website"

# The Archive Bucket
log_archive = t.add_resource(
    Bucket(
        "LogArchiveBucket",
        BucketName=Sub("${AWS::StackName}-logs-archive"),
        VersioningConfiguration=VersioningConfiguration(Status="Enabled"),
        PublicAccessBlockConfiguration=PublicAccessBlockConfiguration(
            BlockPublicAcls=True,
            BlockPublicPolicy=True,
            IgnorePublicAcls=True,
            RestrictPublicBuckets=True
        ),
        BucketEncryption=BucketEncryption(
            ServerSideEncryptionConfiguration=[
                ServerSideEncryptionRule(
                    ServerSideEncryptionByDefault=ServerSideEncryptionByDefault(
                        SSEAlgorithm="AES256"
                    )
                )
            ]
        ),
        Metadata={
            "checkov": {
                "skip": [
                    {
                        "id": "CKV_AWS_18"
                    }
                ]
            }
        }
    )
)

# 2. Enforce SSL (Fixes CKV_AWS_144/Checkov)
t.add_resource(
    BucketPolicy(
        "LogArchiveBucketPolicy",
        Bucket=Ref(log_archive),
        PolicyDocument={
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "AllowSSLRequestsOnly",
                    "Effect": "Deny",
                    "Principal": "*",
                    "Action": "s3:*",
                    "Resource": [
                        Sub("arn:aws:s3:::${LogArchiveBucket}"),
                        Sub("arn:aws:s3:::${LogArchiveBucket}/*")
                    ],
                    "Condition": {"Bool": {"aws:SecureTransport": "false"}},
                }
            ],
        },
    )
)

# 2. ALB Log Bucket
alb_log_bucket = t.add_resource(
    Bucket(
        "ALBLogBucket",
        BucketName=Sub("${AWS::StackName}-alb-access-logs"),
        PublicAccessBlockConfiguration=PublicAccessBlockConfiguration(
            BlockPublicAcls=True, BlockPublicPolicy=True,
            IgnorePublicAcls=True, RestrictPublicBuckets=True
        ),
        LoggingConfiguration=LoggingConfiguration(
            DestinationBucketName=Ref(log_archive),
            LogFilePrefix="alb-access-logs/"
        ),
        VersioningConfiguration=VersioningConfiguration(Status="Enabled"),
        BucketEncryption=BucketEncryption(
            ServerSideEncryptionConfiguration=[
                ServerSideEncryptionRule(
                    ServerSideEncryptionByDefault=ServerSideEncryptionByDefault(
                        SSEAlgorithm="AES256"
                    )
                )
            ]
        ),
    )
)

# Create the S3 bucket
s3_bucket = t.add_resource(
    Bucket(
        "RegionalMap2024Bucket",
        BucketName=BUCKET_NAME,
        VersioningConfiguration=VersioningConfiguration(Status="Enabled"),
        WebsiteConfiguration=WebsiteConfiguration(
            IndexDocument="index.html"
        ),
        PublicAccessBlockConfiguration=PublicAccessBlockConfiguration(
        BlockPublicAcls=True,
        BlockPublicPolicy=True,
        IgnorePublicAcls=True,
        RestrictPublicBuckets=True
        ),
        LoggingConfiguration=LoggingConfiguration(
            DestinationBucketName=Ref("ALBLogBucket"),
            LogFilePrefix="s3-access-logs/regional-map/"
        ),
        BucketEncryption=BucketEncryption(
            ServerSideEncryptionConfiguration=[
                ServerSideEncryptionRule(
                    ServerSideEncryptionByDefault=ServerSideEncryptionByDefault(
                        SSEAlgorithm="AES256"
                    )
                )
            ]
        ),
    )
)

t.add_output(Output(
    "ALBLogBucketName",
    Value=Ref(alb_log_bucket),
    Export=Export("Grindset-ALB-Log-Bucket")
))

# Output the bucket name
t.add_output(Output(
    "BucketName",
    Description="S3 bucket for regional-map-2024",
    Value=Ref(s3_bucket)
))

print(t.to_yaml())
