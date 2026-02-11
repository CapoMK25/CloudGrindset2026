"""
Troposphere template: Cloudwatch demonstration for localstack, fused with checkov
"""

from troposphere import Template, Ref, GetAtt, Export, Output, Sub
import json
from troposphere.kms import Key, Alias # to satisfy checkov
from troposphere.logs import LogGroup, LogStream
from troposphere.cloudwatch import Alarm, MetricDimension, Dashboard

t = Template()
t.set_description("LocalStack CloudWatch setup for an S3 website")

# Log key
log_encryption_key = t.add_resource(
    Key(
        "CloudWatchLogKey",
        Description="KMS Key for CloudWatch Log Group Encryption",
        Enabled=True,
        EnableKeyRotation=True,
        PendingWindowInDays=7,
    )
)

# Alias for the key
t.add_resource(
    Alias(
        "CloudWatchLogKeyAlias",
        AliasName="alias/cloudgrindset-logs",
        TargetKeyId=Ref(log_encryption_key),
    )
)

# Log group
log_group = t.add_resource(LogGroup(
    "DemoLogGroup",
    LogGroupName="cloudgrindset2026-logs",
    RetentionInDays=14,
    KmsKeyId=GetAtt(log_encryption_key, "Arn")
))

# Log stream
log_stream = t.add_resource(LogStream(
    "DemoLogStream",
    LogGroupName=Ref(log_group),
    LogStreamName="demo-stream"
))

# Export for sharing on dynamodb.py
t.add_output(Output(
    "SharedKMSKeyArn",
    Description="KMS Key ARN for encryption",
    Value=GetAtt(log_encryption_key, "Arn"),
    Export=Export(Sub("${AWS::StackName}-KMSKeyArn")),
))

# 1. The Alarm: Triggered if 4xx Errors > 5 in 1 minute
s3_4xx_alarm = t.add_resource(Alarm(
    "S3WebsiteErrorAlarm",
    AlarmDescription="Alarm if S3 bucket returns too many 404s",
    MetricName="4xxErrors",
    Namespace="AWS/S3",
    Statistic="Sum",
    Period="60",
    EvaluationPeriods="1",
    Threshold="5",
    ComparisonOperator="GreaterThanThreshold",
    Dimensions=[
        MetricDimension(Name="BucketName", Value="regional-map-2024-website"),
        MetricDimension(Name="FilterId", Value="EntireBucket")
    ],
))

# 2. The Dashboard: A visual representation of health
dashboard_body = {
    "widgets": [
        {
            "type": "metric",
            "x": 0, "y": 0, "width": 12, "height": 6,
            "properties": {
                "metrics": [
                    ["AWS/S3", "4xxErrors", "BucketName", "regional-map-2024-website"]
                ],
                "period": 300,
                "stat": "Sum",
                "region": "us-east-1",
                "title": "S3 Website 4xx Errors"
            }
        }
    ]
}

t.add_resource(Dashboard(
    "MonitoringDashboard",
    DashboardName="CloudGrindset-S3-Health",
    DashboardBody=json.dumps(dashboard_body)
))

print(t.to_yaml())
