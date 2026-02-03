"""
Troposphere template: DynamoDB dummy for localstack, fixed for checkov
"""

from troposphere import Template, Sub, ImportValue
from troposphere.dynamodb import( 
Table, KeySchema, AttributeDefinition, 
ProvisionedThroughput, PointInTimeRecoverySpecification,
SSESpecification
)

t = Template()
t.set_description("LocalStack DynamoDB table")

table = t.add_resource(Table(
    "DemoTable",
    TableName="cloudgrindset2026",
    AttributeDefinitions=[
        AttributeDefinition(AttributeName="PK", AttributeType="S"),
        AttributeDefinition(AttributeName="SK", AttributeType="S"),
    ],
    KeySchema=[
        KeySchema(AttributeName="PK", KeyType="HASH"),
        KeySchema(AttributeName="SK", KeyType="RANGE"),
    ],
    ProvisionedThroughput=ProvisionedThroughput(
        ReadCapacityUnits=5,
        WriteCapacityUnits=5
    ),
    SSESpecification=SSESpecification(
            SSEEnabled=True,
            SSEType="KMS",
            KMSMasterKeyId=ImportValue(Sub("cloudgrindset-cw-stack-KMSKeyArn"))
        ),
        PointInTimeRecoverySpecification=PointInTimeRecoverySpecification(
        PointInTimeRecoveryEnabled=True
        ),
))

print(t.to_yaml())
