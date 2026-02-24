variable "project_name" {
  description = "The prefix used for naming all resources"
  type        = string
  default     = "CloudGrindset"
}

variable "region" {
  description = "The AWS region for the deployment (localstack-friendly again)"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Deployment environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}