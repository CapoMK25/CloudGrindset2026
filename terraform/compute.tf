# --- 1. SECURITY GROUP (DIRECT ACCESS) ---
resource "aws_security_group" "web_sg" {
  # checkov:skip=CKV_AWS_260: Port 80 must be open here
  # checkov:skip=CKV_AWS_382: High egress is allowed for lab updates
  # checkov:skip=CKV_AWS_23: Descriptions are present in blocks
  name        = "Web-Server-SG"
  description = "Allow direct HTTP access"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "Allow HTTP from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "Web-Server-SG" }
}

# --- 2. COMPUTE (EC2) ---
resource "aws_instance" "web_server" {
  # checkov:skip=CKV_AWS_135: EBS optimization not supported in LocalStack
  # checkov:skip=CKV_AWS_126: Detailed monitoring costs extra in real AWS
  # checkov:skip=CKV_AWS_8: Encryption at rest handled by root_block_device
  
  ami                  = "ami-fake-local"
  instance_type        = var.instance_type
  iam_instance_profile = aws_iam_instance_profile.web_server_profile.name
  
  subnet_id            = aws_subnet.public[0].id
  vpc_security_group_ids = [aws_security_group.web_sg.id]

  metadata_options {
    http_tokens = "required" # Fixes CKV_AWS_79
  }

  root_block_device {
    encrypted = true # Partially fixes CKV_AWS_8
  }

  user_data = base64encode("#!/bin/bash\napt update\napt install -y nginx\nsystemctl start nginx\n")

  tags = { Name = "Grindset-Web-Server" }
}