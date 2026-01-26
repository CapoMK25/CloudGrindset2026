#!/bin/bash
set -e

# Make sure a Python template was passed
if [[ -z "$1" ]]; then
  echo "Usage: ./lab_scripts/generate_templates.sh <iac/template.py>"
  exit 1
fi

IAC_FILE="$1"

# Get the basename of the template, e.g. iam.py -> iam
BASENAME="$(basename "$IAC_FILE" .py)"

# Absolute path to repo root (parent of lab_scripts)
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Path to the YAML folder at root
YAML_DIR="$REPO_ROOT/yaml"

# Make sure the root yaml folder exists
mkdir -p "$YAML_DIR"

# Run the Python template and output to the root yaml folder
python "$REPO_ROOT/$IAC_FILE" > "$YAML_DIR/$BASENAME.yaml"

echo "Generated YAML output in yaml/$BASENAME.yaml"
