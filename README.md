# 🚀 CloudGrindset 2026: The Self-Healing DevOps Ecosystem

CloudGrindset 2026 is a professional-grade Infrastructure-as-Code (IaC) laboratory repo designed to simulate a production-ready AWS environment using LocalStack. This repository demonstrates a complete GitOps lifecycle: from programmatic resource definition to automated security auditing and self-updating documentation.

[![Cloud Grindset Pipeline Status](https://github.com/CapoMK25/CloudGrindset2026/actions/workflows/grindset.yml/badge.svg)](https://github.com/CapoMK25/CloudGrindset2026/actions/workflows/grindset.yml)

## 🏗 Architecture

The diagram below is dynamically generated via Python using the graphviz/diagrams-as-code style setup. Unlike static images, this architecture is a "Living Document" that updates automatically whenever the infrastructure code changes. At least it's supposed to.

![Architecture Diagram](./assets/architecture.png)

## 🛠 The Engineering Core
1. Programmatic Infrastructure (Python Troposphere , Terraform just as a placeholder on this repo)
Moving beyond static YAML, this project utilizes Python-based IaC. The library can be found here: https://github.com/cloudtools/troposphere

Logic-Driven: Uses Python loops and conditionals to manage complex resource relationships.

Type-Safe: Employs strict validation for thresholds and dimensions before a single line of CloudFormation is even generated.

### 2. The Pipeline
This 3-stage CI/CD pipeline ensures that only secure, high-quality code reaches deployment:

Gatekeeper (Lint & Unit Test): Pylint enforces code quality, while Pytest validates the CloudFormation logic.

The Auditor (Checkov): Automated security scanning identifies misconfigurations (e.g., unencrypted logs or wide-open S3 buckets) before they are provisioned.

The Runner (LocalStack): A headless deployment in GitHub Actions simulates a real AWS environment, verifying stack dependencies and S3 synchronization.

### 3. Observability & Self-Healing
The infrastructure isn't finished until it's monitored.

CloudWatch Alarms: Automated provisioning of 4xx error monitoring for S3 website buckets. My previous school project regional-map has been used as the website for this project from the 2024 fork version of the website.

Operational Dashboards: Programmatic generation of CloudWatch Dashboards to visualize system health in real-time.

### 4. Configuration Management (Ansible)
While Troposphere handles the "hardware," Ansible manages the "software." This project uses Ansible playbooks to handle S3 bucket synchronization and website asset management, demonstrating the bridge between Cloud Ops and App Dev.

### 💻 Tech Stack
IaC: Python 3.12, Troposphere

Cloud Emulation: LocalStack

CI/CD: GitHub Actions (custom runner logic)

Security: Checkov, Pylint

Configuration: Ansible

Observability: CloudWatch Metrics & Alarms

Documentation: Diagrams-as-Code (Graphviz)

### 🚀 Getting Started
Prerequisites:

Python 3.12+

Docker (for LocalStack)

AWS CLI & awslocal

One-Click Provisioning:

The "Master Orchestrator" script handles transpilation and sequential deployment to ensure dependency integrity.

### 1. Setup Environment
```Python
python -m venv .venv
source .venv/scripts/activate  # Or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```
### 2. Fire up the local cloud
```
localstack start -d
```
### 3. Deploy the Full Stack
```
./lab_scripts/deploy_all.sh
```

## 📝 Project Evolution & Retrospective
This repository originated as a set of legacy Bash scripts and has evolved into an automated ecosystem.

### Key Technical Challenges:

WSL/Windows Challenges: Solved environment pathing issues to allow Ansible and LocalStack to communicate across virtual boundaries.

Dependency Loops: Implemented a sequential deployment logic to manage cross-stack exports (e.g., VPC IDs required for EC2 Subnets).

CI Bot Identity: Configured GitHub Action bots to sign and push documentation commits, maintaining a clean and automated audit trail.
