#!/bin/bash

# Deploy IAM CloudFormation template to LocalStack, reusable every time when needed

TEMPLATE_FILE="../yaml/iam.yaml"
STACK_NAME="local-iam-lab"
ENDPOINT="http://localhost:4566"

echo "Deploying IAM stack to LocalStack..."

aws --endpoint-url=$ENDPOINT \
    cloudformation create-stack \
    --stack-name $STACK_NAME \
    --template-body file://$TEMPLATE_FILE

echo "Deployment command issued. Check stack status with:"
echo "aws --endpoint-url=$ENDPOINT cloudformation describe-stacks --stack-name $STACK_NAME"