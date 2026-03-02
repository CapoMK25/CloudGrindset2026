# --- 1. ENCRYPTION (KMS) ---

resource "aws_kms_key" "log_key" {
  description             = "KMS Key for CloudWatch Log Group Encryption"
  deletion_window_in_days = 7
  enable_key_rotation     = true

  tags = { Name = "CloudGrindset-Log-Key" }
}

resource "aws_kms_alias" "log_key_alias" {
  name          = "alias/cloudgrindset-logs"
  target_key_id = aws_kms_key.log_key.key_id
}

# --- 2. LOGS ---

resource "aws_cloudwatch_log_group" "demo_log_group" {
  name              = "cloudgrindset2026-logs"
  retention_in_days = 14
  # kms_key_id        = aws_kms_key.log_key.arn
}

resource "aws_cloudwatch_log_stream" "demo_stream" {
  name           = "demo-stream"
  log_group_name = aws_cloudwatch_log_group.demo_log_group.name
}

# --- 3. ALARMS ---

resource "aws_cloudwatch_metric_alarm" "s3_4xx_alarm" {
  alarm_name          = "S3WebsiteErrorAlarm"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "4xxErrors"
  namespace           = "AWS/S3"
  period              = "60"
  statistic           = "Sum"
  threshold           = "5"
  alarm_description   = "Alarm if S3 bucket returns too many 404s"

  dimensions = {
    BucketName = "regional-map-2024-website"
    FilterId   = "EntireBucket"
  }
}

# --- 4. DASHBOARD ---

resource "aws_cloudwatch_dashboard" "main" {
  dashboard_name = "CloudGrindset-S3-Health"

  dashboard_body = <<EOF
{
  "widgets": [
    {
      "type": "metric",
      "x": 0, "y": 0, "width": 12, "height": 6,
      "properties": {
        "metrics": [
          ["AWS/S3", "4xxErrors", "BucketName", "regional-map-2024-website"]
        ],
        "period": 300,
        "stat": "Sum",
        "region": "us-east-1",
        "title": "S3 Website 4xx Errors"
      }
    }
  ]
}
EOF
}

# --- 5. OUTPUTS ---

output "shared_kms_key_arn" {
  value       = aws_kms_key.log_key.arn
  description = "KMS Key ARN for encryption across the module"
}