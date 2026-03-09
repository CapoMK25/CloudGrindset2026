# --- 1. SLEEP TIMER ---
# This forces a 30-second pause to allow LocalStack's internal 
# state to synchronize IAM and networking.
resource "time_sleep" "wait_for_iam_and_network" {
  depends_on = [
    aws_iam_instance_profile.web_server_profile,
    aws_subnet.public,
    aws_security_group.web_sg,
    aws_route_table_association.public
  ]

  create_duration = "30s"
}

# --- 2. EC2 ---
resource "aws_instance" "web_server" {
  # checkov:skip=CKV_AWS_135: EBS optimization not supported in LocalStack
  depends_on = [
    time_sleep.wait_for_iam_and_network,
    aws_subnet.public,
    aws_iam_instance_profile.web_server_profile,
    aws_security_group.web_sg
  ]

  ami                  = "ami-df5ccb86"
  instance_type        = "t2.micro"
  ebs_optimized        = true      
  iam_instance_profile = aws_iam_instance_profile.web_server_profile.name
  monitoring           = true
  
  subnet_id              = aws_subnet.public[0].id
  vpc_security_group_ids = [aws_security_group.web_sg.id]

  metadata_options {
    http_tokens   = "required"
    http_endpoint = "enabled"
  }

  root_block_device {
    encrypted = true
  }

  user_data = base64encode("#!/bin/bash\necho 'Hello World' > /tmp/hello")

  tags = { Name = "Grindset-Web-Server" }
}