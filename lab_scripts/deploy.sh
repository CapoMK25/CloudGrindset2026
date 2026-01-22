#!/bin/bash
# Deploy all YAML CloudFormation templates in the yaml folder to LocalStack
# Cross-platform: works on GitHub Actions (Linux) and Windows Git Bash

ENDPOINT_URL="http://localhost:4566"

# Resolve repo root (script is in lab_scripts/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
YAML_DIR="$REPO_ROOT/yaml"

echo "Using YAML directory: $YAML_DIR"

if [ ! -d "$YAML_DIR" ]; then
    echo "YAML folder not found: $YAML_DIR"
    exit 1
fi

# Enable nullglob to handle empty folders gracefully
shopt -s nullglob

for yaml_file in "$YAML_DIR"/*.yaml; do
    stack_name=$(basename "$yaml_file" .yaml)

    # Detect Windows Git Bash and convert path if needed
    if command -v cygpath >/dev/null 2>&1; then
        TEMPLATE_PATH=$(cygpath -w "$yaml_file")
    else
        TEMPLATE_PATH="$yaml_file"
    fi

    echo "Deploying stack: $stack_name"

    # --------------------------
    # Delete existing stack if it exists
    # --------------------------
    if aws --endpoint-url="$ENDPOINT_URL" cloudformation describe-stacks \
        --stack-name "$stack_name" >/dev/null 2>&1; then

        echo "Stack $stack_name exists, deleting before redeploy..."
        aws --endpoint-url="$ENDPOINT_URL" cloudformation delete-stack \
            --stack-name "$stack_name" 2>/dev/null || true

        aws --endpoint-url="$ENDPOINT_URL" cloudformation wait stack-delete-complete \
            --stack-name "$stack_name" 2>/dev/null || true

        echo "Stack $stack_name deleted"
    fi

    # --------------------------
    # Create new stack
    # --------------------------
    echo "Creating stack: $stack_name"
    aws --endpoint-url="$ENDPOINT_URL" cloudformation create-stack \
        --stack-name "$stack_name" \
        --template-body "file://$TEMPLATE_PATH" \
        --capabilities CAPABILITY_NAMED_IAM

    aws --endpoint-url="$ENDPOINT_URL" cloudformation wait stack-create-complete \
        --stack-name "$stack_name"

    echo "Stack $stack_name deployed"
done

echo "All YAML stacks deployed"
