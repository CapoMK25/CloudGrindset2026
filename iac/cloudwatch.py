"""
Troposphere template: Cloudwatch demonstration for localstack, fused with checkov
"""

from troposphere import Template, Ref, GetAtt, Export, Output, Sub
from troposphere.kms import Key, Alias # to satisfy checkov
from troposphere.logs import LogGroup, LogStream

t = Template()
t.set_description("LocalStack CloudWatch Logs setup")

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

print(t.to_yaml())
