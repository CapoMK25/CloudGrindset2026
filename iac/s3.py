"""
Troposphere template: S3 bucket for regional-map-2024 website
Works with LocalStack
"""

from troposphere import Template, Ref, Output
from troposphere.s3 import (
    Bucket,
    WebsiteConfiguration,
    VersioningConfiguration,
    PublicAccessBlockConfiguration
)

# Create the template
t = Template()
t.set_description("LocalStack S3 bucket for regional-map-2024 hosting")

# Bucket name
BUCKET_NAME = "regional-map-2024-website"

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
        )
    )
)

# Output the bucket name
t.add_output(Output(
    "BucketName",
    Description="S3 bucket for regional-map-2024",
    Value=Ref(s3_bucket)
))

print(t.to_yaml())
