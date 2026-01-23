"""
Troposphere template: DynamoDB dummy for localstack
"""

from troposphere import Template
from troposphere.dynamodb import Table, KeySchema, AttributeDefinition, ProvisionedThroughput

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
    )
))

print(t.to_yaml())
