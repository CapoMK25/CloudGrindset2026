resource "aws_dynamodb_table" "state_table" {
  name           = "regional-map-2024"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "UserId"

  attribute {
    name = "UserId"
    type = "S"
  }

  tags = { Environment = "Dev" }
}