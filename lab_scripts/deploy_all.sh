#!/bin/bash
set -e

# --- 1. Environment & Setup ---
export AWS_DEFAULT_REGION=us-east-1
export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID:-test}
export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY:-test}
ENDPOINT_URL="http://localhost:4566"

# Absolute paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
IAC_DIR="$REPO_ROOT/iac"
YAML_DIR="$REPO_ROOT/yaml"

# Safety net for deployment
mkdir -p "$YAML_DIR"

echo "Starting 2026 Cloud Grindset Deployment..."
echo "--------------------------------------------"

# --- 2. Helper Functions ---

# Function to generate YAML from Python Troposphere templates
generate_yaml() {
    local py_file=$1
    local base_name=$(basename "$py_file" .py)
    echo "Generating: $base_name.yaml"
    python "$py_file" > "$YAML_DIR/$base_name.yaml"
}

# Function to deploy a stack
deploy_stack() {
    local stack_name=$1
    local yaml_file="$YAML_DIR/$stack_name.yaml"
    
    # Path conversion for Windows/Git Bash
    if command -v cygpath >/dev/null 2>&1; then
        TEMPLATE_PATH=$(cygpath -w "$yaml_file")
    else
        TEMPLATE_PATH="$yaml_file"
    fi

    echo "Deploying Stack: $stack_name"

    # Delete if it exists to ensure a clean state
    if aws --endpoint-url="$ENDPOINT_URL" cloudformation describe-stacks --stack-name "$stack_name" >/dev/null 2>&1; then
        echo "   - Existing stack found. Deleting..."
        aws --endpoint-url="$ENDPOINT_URL" cloudformation delete-stack --stack-name "$stack_name"
        aws --endpoint-url="$ENDPOINT_URL" cloudformation wait stack-delete-complete --stack-name "$stack_name"
    fi

    # Create new stack
    aws --endpoint-url="$ENDPOINT_URL" cloudformation create-stack \
        --stack-name "$stack_name" \
        --template-body "file://$TEMPLATE_PATH" \
        --capabilities CAPABILITY_NAMED_IAM

    echo "   - Waiting for creation..."
    aws --endpoint-url="$ENDPOINT_URL" cloudformation wait stack-create-complete --stack-name "$stack_name"
    echo "$stack_name Deployed."
}

# --- 3. Step 1: Generate All Templates ---
echo "Step 1: Transpiling Troposphere to YAML..."
for f in "$IAC_DIR"/*.py; do
    generate_yaml "$f"
done
echo "--------------------------------------------"

# --- 4. Step 2: Ordered Deployment ---
# Defining the order manually because of ImportValue dependencies
echo "Step 2: Orchestrating CloudFormation..."

# Level 1: Core Networking (VPC, Subnets)
deploy_stack "networking"

# Level 2: Identity & Access (Roles, Instance Profiles)
deploy_stack "iam"

# Level 3: Application Resources (EC2, S3, DynamoDB, Logs)
# These depend on Networking and IAM existing first
deploy_stack "ec2"
deploy_stack "s3"
deploy_stack "dynamodb"
deploy_stack "cloudwatch"

echo "--------------------------------------------"
echo "ALL SYSTEMS ONLINE"
echo "EC2 is running, S3 Website is live, and IAM is wired."