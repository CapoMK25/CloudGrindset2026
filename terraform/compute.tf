# --- 1. SECURITY GROUPS ---

# ALB Security Group (Public)
# checkov:skip=CKV_AWS_260: ALB must be open on port 80 for public web traffic.
resource "aws_security_group" "alb_sg" {
  name        = "ALB-SG"
  description = "Public internet access for the Load Balancer"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "Allow HTTP from the Internet"
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

  tags = { Name = "ALB-SG" }
}

# Web Server Security Group (Private-ish)
resource "aws_security_group" "web_sg" {
  name        = "Web-Server-SG"
  description = "Allow ONLY ALB access"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "Allow HTTP traffic from ALB SG only"
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.alb_sg.id]
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
  ami                  = "ami-fake-local" # LocalStack dummy AMI
  instance_type        = var.instance_type
  iam_instance_profile = aws_iam_instance_profile.web_server_profile.name
  subnet_id = aws_subnet.public[0].id
  vpc_security_group_ids = [aws_security_group.web_sg.id]

  user_data = base64encode("#!/bin/bash\napt update\napt install -y nginx\n")

  tags = { Name = "Grindset-Web-Server" }
}

# --- 3. LOAD BALANCING (ALB) ---

resource "aws_lb_target_group" "web_tg" {
  name     = "WebTargetGroup"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
  target_type = "instance"
}

resource "aws_lb_target_group_attachment" "web_tg_attach" {
  target_group_arn = aws_lb_target_group.web_tg.arn
  target_id        = aws_instance.web_server.id
  port             = 80
}

resource "aws_lb" "web_alb" {
  name               = "Grindset-Web-ALB"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets = aws_subnet.public[*].id

  access_logs {
    bucket  = "regional-map-2024-website"
    prefix  = "alb-logs"
    enabled = true
  }

  drop_invalid_header_fields = true

  tags = { Name = "Grindset-Web-ALB" }
}

# --- 4. LISTENER ---

# checkov:skip=CKV_AWS_2: Using HTTP for localstack/demo purposes.
# checkov:skip=CKV_AWS_103: TLS 1.2 not applicable for the HTTP listener.
resource "aws_lb_listener" "web_listener" {
  load_balancer_arn = aws_lb.web_alb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web_tg.arn
  }
}