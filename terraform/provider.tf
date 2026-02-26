# /terraform/provider.tf

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region     = "us-east-1"
  access_key = "test"
  secret_key = "test"

  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  s3_use_path_style           = true

  endpoints {
    ec2      = "http://localhost:4566"
    elb      = "http://localhost:4566"
    elbv2    = "http://localhost:4566"
    kms      = "http://localhost:4566" 
    iam      = "http://localhost:4566"
    s3       = "http://s3.localhost.localstack.cloud:4566"
    dynamodb = "http://localhost:4566"
    logs     = "http://localhost:4566"
    cloudwatch = "http://localhost:4566"
  }
}