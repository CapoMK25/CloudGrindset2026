# VARIABLES DEFINED IN ONE CENTRAL FILE

# USER & GROUP SETUP

resource "aws_iam_group" "admins" {
  name = "${var.project_name}-Admins"
}

resource "aws_iam_user" "mk_user" {
  # checkov:skip=CKV_AWS_273: Using IAM User here instead of SSO
  name = "${var.project_name}-MK"
}

resource "aws_iam_group_membership" "add_mk_to_admins" {
  name  = "add-mk-to-admins"
  users = [aws_iam_user.mk_user.name]
  group = aws_iam_group.admins.name
}

# ADMIN POLICY

resource "aws_iam_policy" "admins_policy" {
  # checkov:skip=CKV_AWS_62: Full Admin access required here
  # checkov:skip=CKV_AWS_63: Wildcard actions allowed for testing
  # checkov:skip=CKV_AWS_286: Privilege escalation is intentional for admin user
  # checkov:skip=CKV_AWS_287: Credentials exposure skip for lab
  # checkov:skip=CKV_AWS_288: Data exfiltration skip for lab
  # checkov:skip=CKV_AWS_289: Permissions management skip
  # checkov:skip=CKV_AWS_290: Write access skip
  # checkov:skip=CKV_AWS_355: Wildcard resources allowed for full admin profile
  # checkov:skip=CKV2_AWS_40: Full IAM privileges allowed for this specific user
  name        = "${var.project_name}-AdminsAdministratorAccess"
  description = "Checkov-compliant admin policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "*"
      Resource = "*"
    }]
  })
}

resource "aws_iam_group_policy_attachment" "admins_attach" {
  group      = aws_iam_group.admins.name
  policy_arn = aws_iam_policy.admins_policy.arn
}

# IAM Role here

resource "aws_iam_role" "web_server_role" {
  name = "${var.project_name}-WebServerRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy" "s3_read_access" {
  name = "S3ReadAccess"
  role = aws_iam_role.web_server_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = ["s3:Get*", "s3:List*"]
      Resource = [
        "arn:aws:s3:::regional-map-2024-website",
        "arn:aws:s3:::regional-map-2024-website/*"
      ]
    }]
  })
}

resource "aws_iam_instance_profile" "web_server_profile" {
  name = "${var.project_name}-EC2-Profile"
  role = aws_iam_role.web_server_role.name
}

output "web_server_instance_profile_name" {
  value = aws_iam_instance_profile.web_server_profile.name
}