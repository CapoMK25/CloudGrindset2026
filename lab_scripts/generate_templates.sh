#!/bin/bash

# Make sure your virtual environment is active first
# source .venv/Scripts/activate  (Windows Git Bash)
# source .venv/bin/activate      (Linux/WSL)

# Check if a Python file is provided as argument
if [ -z "$1" ]; then
    echo "Usage: $0 <python_template.py>"
    exit 1
fi

# Get input Python file and its basename
PY_FILE="$1"
BASENAME=$(basename "$PY_FILE" .py)

# Build output YAML path
YAML_FILE="yaml/$BASENAME.yaml"

# Generate YAML
python "$PY_FILE" > "$YAML_FILE"

echo "Generated YAML output in $YAML_FILE"
