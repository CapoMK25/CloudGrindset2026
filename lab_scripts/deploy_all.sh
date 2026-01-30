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
# Path to regional-map repo on the Desktop
WEBSITE_CONTENT_DIR="$(cd "$REPO_ROOT/.." && pwd)/regional-map-2024"

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
echo "Step 2: Orchestrating CloudFormation..."

deploy_stack "networking"
deploy_stack "iam"
deploy_stack "ec2"
deploy_stack "s3"
deploy_stack "dynamodb"
deploy_stack "cloudwatch"

echo "--------------------------------------------"

# --- 5. Step 3: Sync Website Content ---
echo "Step 3: Syncing Website Assets..."

if [ -d "$WEBSITE_CONTENT_DIR" ]; then
    echo "   - Uploading content from $WEBSITE_CONTENT_DIR"
    aws --endpoint-url="$ENDPOINT_URL" s3 sync "$WEBSITE_CONTENT_DIR" s3://regional-map-2024-website/ --exclude ".git/*"
    echo "   - Sync Complete."
else
    echo "   - Error: Website content directory not found at $WEBSITE_CONTENT_DIR"
    echo "   - Skipping S3 sync."
fi

echo "--------------------------------------------"
echo "ALL SYSTEMS ONLINE"
echo "EC2 is running, S3 Website is live, and IAM is wired."
echo "URL: http://localhost:4566/regional-map-2024-website/index.html"