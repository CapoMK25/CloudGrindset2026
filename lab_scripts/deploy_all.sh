#!/bin/bash
set -e

# --- 1. Environment & Setup ---
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
echo "--------------------------------------------"

# --- 2. Helper Functions ---
generate_yaml() {
    local py_file=$1
    local base_name=$(basename "$py_file" .py)
    echo "Generating: $base_name.yaml"
    python "$py_file" > "$YAML_DIR/$base_name.yaml"
}

deploy_stack() {
    local stack_name=$1
    echo "Deploying Stack: $stack_name..."

    if aws --endpoint-url="$ENDPOINT_URL" cloudformation deploy \
        --stack-name "$stack_name" \
        --template-file "$YAML_DIR/$stack_name.yaml" \
        --capabilities CAPABILITY_NAMED_IAM \
        --no-fail-on-empty-changeset; then
        echo "$stack_name Deployed Successfully."
    else
        echo "Error: Failed to deploy $stack_name"
        exit 1
    fi
}

# --- 3. Step 1: Generate All Templates ---
for f in "$IAC_DIR"/*.py; do
    generate_yaml "$f"
done

# --- 4. Step 2: Ordered Deployment ---
# These must exist as .py files in your iac/ folder!
deploy_stack "networking"
deploy_stack "iam"
deploy_stack "s3"
deploy_stack "ec2"
deploy_stack "dynamodb"
deploy_stack "cloudwatch"

# --- 5. Step 3: Sync Website Content ---
if [ -d "$WEBSITE_CONTENT_DIR" ]; then
    echo "Syncing Website Assets..."
    aws --endpoint-url="$ENDPOINT_URL" s3 sync "$WEBSITE_CONTENT_DIR" s3://regional-map-2024-website/ --exclude ".git/*"
    echo "Sync Complete."
else
    echo "Error: Website content directory not found at $WEBSITE_CONTENT_DIR"
    exit 1
fi

echo "--------------------------------------------"
echo "ALL SYSTEMS ONLINE"
echo "URL: http://localhost:4566/regional-map-2024-website/index.html"