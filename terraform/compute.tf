# --- 1. SECURITY GROUP (DIRECT ACCESS) ---
resource "aws_security_group" "web_sg" {
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
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "Web-Server-SG" }
}

# --- 2. COMPUTE (EC2) ---

resource "aws_instance" "web_server" {
  ami                  = "ami-fake-local"
  instance_type        = var.instance_type
  iam_instance_profile = aws_iam_instance_profile.web_server_profile.name
  subnet_id            = aws_subnet.public[0].id
  vpc_security_group_ids = [aws_security_group.web_sg.id]

  # Install Nginx automatically
  user_data = base64encode("#!/bin/bash\napt update\napt install -y nginx\nsystemctl start nginx\n")

  depends_on = [
    aws_subnet.public,
    aws_security_group.web_sg,
    aws_iam_instance_profile.web_server_profile,
    aws_internet_gateway.igw,
    aws_route_table_association.public,
    aws_iam_role_policy.s3_read_access, 
    aws_security_group.web_sg  
  ]

  tags = { Name = "Grindset-Web-Server" }
}