# 1. THE LOG ARCHIVE BUCKET
resource "aws_s3_bucket" "log_archive" {
  # checkov:skip=CKV_AWS_144: Cross-region replication not needed here
  # checkov:skip=CKV_AWS_145: KMS encryption not supported in LocalStack
  # checkov:skip=CKV2_AWS_61: Lifecycle configuration not required for this demo
  # checkov:skip=CKV2_AWS_62: Event notifications not required
  bucket = "cloudgrindset-logs-archive"
}

resource "aws_s3_bucket_versioning" "log_archive_versioning" {
  bucket = aws_s3_bucket.log_archive.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "log_archive_crypto" {
  bucket = aws_s3_bucket.log_archive.id
  rule {
    apply_server_side_encryption_by_default { sse_algorithm = "AES256" }
  }
}

resource "aws_s3_bucket_public_access_block" "log_archive_lockdown" {
  bucket                  = aws_s3_bucket.log_archive.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# 2. THE SSL ENFORCEMENT POLICY
resource "aws_s3_bucket_policy" "log_archive_ssl_only" {
  bucket = aws_s3_bucket.log_archive.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid       = "AllowSSLRequestsOnly"
      Effect    = "Deny"
      Principal = "*"
      Action    = "s3:*"
      Resource = [
        aws_s3_bucket.log_archive.arn,
        "${aws_s3_bucket.log_archive.arn}/*"
      ]
      Condition = {
        Bool = { "aws:SecureTransport" = "false" }
      }
    }]
  })
}

# 3. REGIONAL MAP WEBSITE BUCKET
resource "aws_s3_bucket" "website" {
  # checkov:skip=CKV_AWS_144: Cross-region replication not required
  # checkov:skip=CKV_AWS_145: KMS encryption skipped for LocalStack compatibility
  # checkov:skip=CKV_AWS_21: Versioning intentionally disabled to keep local storage light
  # checkov:skip=CKV2_AWS_6: Public access block would prevent the website from being viewable
  # checkov:skip=CKV2_AWS_61: Lifecycle configuration not required
  # checkov:skip=CKV2_AWS_62: Event notifications not required
  bucket = "regional-map-2024-website"
}

resource "aws_s3_bucket_website_configuration" "website_config" {
  bucket = aws_s3_bucket.website.id
  index_document { suffix = "index.html" }
}

resource "aws_s3_bucket_logging" "website_logging" {
  bucket        = aws_s3_bucket.website.id
  target_bucket = aws_s3_bucket.log_archive.id
  target_prefix = "s3-access-logs/regional-map/"
}