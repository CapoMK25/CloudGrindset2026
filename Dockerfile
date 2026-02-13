# Use the slim Python image as the base
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install 'curl' and 'awscli' (or awslocal) needed for the .sh script
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    bash \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

# Requirements to run the thing
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Grant execution permissions
RUN chmod +x lab_scripts/deploy_all.sh

# ENV variables
ENV AWS_ACCESS_KEY_ID=test
ENV AWS_SECRET_ACCESS_KEY=test
ENV AWS_DEFAULT_REGION=us-east-1

# Set the command to run the main deploy script
CMD ["/bin/bash", "lab_scripts/deploy_all.sh"]