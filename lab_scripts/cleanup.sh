#!/bin/bash
set -e

# --- 1. Environment & Setup ---
export AWS_DEFAULT_REGION=us-east-1
export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID:-test}
export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY:-test}
ENDPOINT_URL="http://localhost:4566"

echo "Initializing 2026 Cloud Grindset Cleanup..."
echo "--------------------------------------------"

# --- 2. Helper Functions ---

# Function to delete a stack with a safety check
delete_stack() {
    local stack_name=$1
    
    if aws --endpoint-url="$ENDPOINT_URL" cloudformation describe-stacks --stack-name "$stack_name" >/dev/null 2>&1; then
        echo "Deleting Stack: $stack_name"
        
        # Special handling for S3: CloudFormation won't delete a non-empty bucket
        if [ "$stack_name" == "s3" ]; then
            echo "   - Emptying S3 bucket: regional-map-2024-website..."
            aws --endpoint-url="$ENDPOINT_URL" s3 rm s3://regional-map-2024-website --recursive >/dev/null 2>&1 || true
        fi

        aws --endpoint-url="$ENDPOINT_URL" cloudformation delete-stack --stack-name "$stack_name"
        
        echo "   - Waiting for deletion to complete..."
        aws --endpoint-url="$ENDPOINT_URL" cloudformation wait stack-delete-complete --stack-name "$stack_name"
        echo "   - $stack_name removed."
    else
        echo "Stack $stack_name not found, skipping."
    fi
}

# --- 3. Reverse Order Deletion (LIFO) ---

echo "Step 1: Removing Application Layer..."
delete_stack "cloudwatch"
delete_stack "dynamodb"
delete_stack "s3"
delete_stack "ec2"

echo "--------------------------------------------"

echo "Step 2: Removing Identity Layer..."
delete_stack "iam"

echo "--------------------------------------------"

echo "Step 3: Removing Core Networking..."
delete_stack "networking"

echo "--------------------------------------------"
echo "CLEANUP COMPLETE"
echo "LocalStack is now a blank canvas. Your local files (iac/ and yaml/) are safe."