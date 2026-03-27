#!/bin/bash
set -e

# --- 1. Local Environment ---
export AWS_DEFAULT_REGION=us-east-1
export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID:-test}
export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY:-test}

ENDPOINT_URL="${AWS_ENDPOINT_URL:-http://localhost:4566}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
IAC_DIR="$REPO_ROOT/iac"
YAML_DIR="$REPO_ROOT/yaml"
WEBSITE_CONTENT_DIR="${WEBSITE_CONTENT_DIR:-$REPO_ROOT/regional-map-2024}"

mkdir -p "$YAML_DIR"

echo "Starting 2026 Cloud Grindset Deployment..."
echo "Endpoint: $ENDPOINT_URL"

# --- 2. Helper Functions ---
generate_yaml() {
    local py_file=$1
    local base_name=$(basename "$py_file" .py)
    echo "Generating: $base_name.yaml"
    python "$py_file" > "$YAML_DIR/$base_name.yaml"
}

deploy_stack() {
    local stack_name=$1
    local log_file="deploy_${stack_name}_error.log"

    echo "Deploying Stack: $stack_name..."

    if aws --endpoint-url="$ENDPOINT_URL" cloudformation deploy \
        --stack-name "$stack_name" \
        --template-file "$YAML_DIR/$stack_name.yaml" \
        --capabilities CAPABILITY_NAMED_IAM \
        --no-fail-on-empty-changeset 2> "$log_file"; then
        
        echo "$stack_name Deployed Successfully!"
        rm -f "$log_file" # Delete the log file when successful
    else
        echo "Failed to deploy $stack_name"
        echo "Detailed AWS Error Logs:"
        cat "$log_file"
        
        # Deletion
        rm -f "$log_file"
        
        exit 1
    fi
}

# --- 3. Step 1: Generate All Templates ---
for f in "$IAC_DIR"/*.py; do
    generate_yaml "$f"
done

# --- 4. Deployment ---
deploy_stack "networking"   # Provides VPC/Subnets
deploy_stack "iam"          # Provides Roles/Profiles
deploy_stack "cloudwatch"   # PROVIDE KMS KEYS & LOG GROUPS FIRST
deploy_stack "s3"           # Provides Buckets
deploy_stack "dynamodb"     # Uses KMS from cloudwatch
deploy_stack "ec2"          # Uses IAM, Networking, and KMS
deploy_stack "dns"          # Final routing

# --- 5. Sync Website Content ---
if [ -d "$WEBSITE_CONTENT_DIR" ]; then
    echo "Syncing Website Files..."
    aws --endpoint-url="$ENDPOINT_URL" s3 sync "$WEBSITE_CONTENT_DIR" s3://regional-map-2024-website/ --exclude ".git/*"
    echo "Sync Complete."
else
    echo "Error: Website content directory not found at $WEBSITE_CONTENT_DIR"
    exit 1
fi

echo "ALL STACKS ONLINE!"
echo "URL: http://localhost:4566/regional-map-2024-website/index.html"