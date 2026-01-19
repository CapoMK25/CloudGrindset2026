#!/bin/bash

# Make sure venv is active first

python iac/nginx.py > yaml/nginx.yaml

echo "Generated YAML in yaml/nginx.yaml"
