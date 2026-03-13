# Enforcing a baseline here, as uncovered by Trivy locally
FROM debian:13.3

# Baseline updates here to kick off this Dockerfile
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 1. Base stage for dependencies
FROM python:3.11-slim-bookworm AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Prod
FROM python:3.11-slim-bookworm
WORKDIR /app

# Install only the "runtime" tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    bash \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

# Copy the installed packages from the builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copying to be done here only
COPY . .
RUN chmod +x lab_scripts/deploy_all.sh

CMD ["/bin/bash", "lab_scripts/deploy_all.sh"]