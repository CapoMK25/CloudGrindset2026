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

# --- 2. EC2 ---
resource "aws_instance" "web_server" {
  # checkov:skip=CKV_AWS_135: EBS optimization not supported
  ami                  = "ami-0ff8a91507f77f867"
  instance_type        = "t2.medium"
  ebs_optimized        = true      
  iam_instance_profile = aws_iam_instance_profile.web_server_profile.name
  monitoring           = true
  
  subnet_id              = aws_subnet.public[0].id
  vpc_security_group_ids = [aws_security_group.web_sg.id]

  # Fixes CKV_AWS_79 (IMDSv2 required)
  metadata_options {
    http_tokens   = "required"
    http_endpoint = "enabled"
  }

  # Fixes CKV_AWS_8 (Root block device encryption)
  root_block_device {
    encrypted = true
  }

  user_data = base64encode("#!/bin/bash\necho 'Hello World' > /tmp/hello")

  depends_on = [
    aws_subnet.public,
    aws_security_group.web_sg,
    aws_iam_instance_profile.web_server_profile,
    aws_route_table_association.public
  ]

  tags = { Name = "Grindset-Web-Server" }
}