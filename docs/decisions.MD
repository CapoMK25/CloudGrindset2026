Decided to update the localstack environment to run it locally.

The end goal from here on out is the following: 

Troposphere → YAML → CloudFormation → LocalStack → AWS CLI → observable state → CI/CD set up to automate the process and add linting

# 20.1.2026

- Installed the basics of NGINX to a Linux server
- Updated the bash script to do said things
- Installed localstack to simulate AWS locally via the terminal on Git Bash
- Ran IaC through localstack
- Confirmed the templates work
- Pushed everything to GitHub to update this repo
- Created an IAM user and other IAM basics for this setup via IaC
- Installed the AWS CLI and other trinkets to Ubuntu Server running on WSL

Confirmed as running here: 

capomk@DESKTOP-2SBTD6B:~/tmp/awscli-install$ aws --endpoint-url=http://localhost:4566 iam list-users
{
    "Users": [
        {
            "Path": "/",
            "UserName": "MK",
            "UserId": "gwlcyhh9qkrxwt74iga0",
            "Arn": "arn:aws:iam::000000000000:user/MK",
            "CreateDate": "2026-01-20T12:39:44.307812+00:00"
        }
    ]
}


# 21.1.2026

Linting to be added with GitHub Actions