# DYNAMODB TABLE

resource "aws_dynamodb_table" "demo_table" {
  # checkov:skip=CKV2_AWS_16: Auto-scaling not needed here
  # checkov:skip=CKV_AWS_28: PITR is enabled below, but skipping to ensure parser alignment
  
  name           = "cloudgrindset2026"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5

  # Partition Key (HASH) and Sort Key (RANGE)
  hash_key  = "PK"
  range_key = "SK"

  attribute {
    name = "PK"
    type = "S"
  }

  attribute {
    name = "SK"
    type = "S"
  }

  # Point-in-time recovery (PITR)
  point_in_time_recovery {
    enabled = true
  }

  # Server-Side Encryption
  server_side_encryption {
    enabled     = true
    kms_key_arn = aws_kms_key.log_key.arn
  }

  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}