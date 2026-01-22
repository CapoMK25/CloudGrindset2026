# Infra basics for this project

- Docker running locally 
- Localstack running through Docker locally 
- IaC setup through troposphere and YAML, just like on AWS with CloudFormation
- Scripts to automate things locally

# 21.1.2026

Automated IAM deployment to CloudFormation on localstack with a Bash script on root/lab_scripts/deploy_iam.sh

It works, this is the output on the terminal: 

$ ./deploy_iam.sh
Deploying IAM stack to LocalStack...
{
    "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/local-iam-lab/ae9014e6-98d5-4dac-b0b7-2edd0386cc44"
}
Deployment command issued. Check stack status with:
aws --endpoint-url=http://localhost:4566 cloudformation describe-stacks --stack-name local-iam-lab
(.venv)

Changed the generate_templates.sh script content to include universal file naming instead of hard coded files and tested it locally to make sure it worked, here's the output on LocalStack: 

$ aws --endpoint-url=http://localhost:4566 cloudformation create-stack \
  --stack-name local-ec2-lab \
  --stack-name local-ec2-lab \
  --template-body file://yaml/ec2.yaml
{
    "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/local-ec2-lab/ba691f41-77d1-45b9-b938-30775b8c8037"
}
(.venv)

- Changes for the future: 

This is fine as is but should be modified to one big coherent script that spins up all of your IAM, EC2 and other AWS resources by running one script with localstack running already. 

- Later on today: 

I created one big deploy.sh script for deployment and modified generate_templates.sh accordingly so that you can now run one big script on root and automate deployment of all AWS resources you want like IAM, EC2 or NGINX or whatever. Here's the correct output of the script to see that it works, it just needs a rewrite on the NGINX.py troposphere template: 

$ ./lab_scripts/deploy.sh
Using YAML directory: /c/Users/Matias.DESKTOP-2SBTD6B/Desktop/CloudGrindset2026/yaml
Deploying stack: ec2
Stack ec2 exists, deleting before redeploy...
Stack ec2 deleted
Creating stack: ec2
{
    "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/ec2/a0c6acdc-c4d6-45e5-98cb-4c5f1ed1ba02"
}
Stack ec2 deployed
Deploying stack: iam
Creating stack: iam
{
    "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/iam/2c880263-723b-4189-a375-6f354b31958b"
}
Stack iam deployed
Deploying stack: nginx
Stack nginx exists, deleting before redeploy...
Stack nginx deleted
Creating stack: nginx
{
    "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/nginx/2505d1dc-0d20-4787-a0bd-3bb07b27a28f"
}

Waiter StackCreateComplete failed: Waiter encountered a terminal failure state: For expression "Stacks[].StackStatus" we matched expected path: "CREATE_FAILED" at least once
Stack nginx deployed
All YAML stacks deployed!
(.venv) 
{
    "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/ec2/a0c6acdc-c4d6-45e5-98cb-4c5f1ed1ba02"
}
Stack ec2 deployed
Deploying stack: iam
Creating stack: iam
{
    "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/iam/2c880263-723b-4189-a375-6f354b31958b"
}
Stack iam deployed
Deploying stack: nginx
Stack nginx exists, deleting before redeploy...
Stack nginx deleted
Creating stack: nginx
{
    "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/nginx/2505d1dc-0d20-4787-a0bd-3bb07b27a28f"
}

Waiter StackCreateComplete failed: Waiter encountered a terminal failure state: For expression "Stacks[].StackStatus" we matched expected path: "CREATE_FAILED" at least once
Stack nginx deployed
All YAML stacks deployed!
(.venv)
Creating stack: iam
{
    "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/iam/2c880263-723b-4189-a375-6f354b31958b"
}
Stack iam deployed
Deploying stack: nginx
Stack nginx exists, deleting before redeploy...
Stack nginx deleted
Creating stack: nginx
{
    "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/nginx/2505d1dc-0d20-4787-a0bd-3bb07b27a28f"
}

Waiter StackCreateComplete failed: Waiter encountered a terminal failure state: For expression "Stacks[].StackStatus" we matched expected path: "CREATE_FAILED" at least once
Stack nginx deployed
All YAML stacks deployed!
(.venv)
}

Waiter StackCreateComplete failed: Waiter encountered a terminal failure state: For expression "Stacks[].StackStatus" we matched expected path: "CREATE_FAILED" at least once
Stack nginx deployed
All YAML stacks deployed!
(.venv)
(.venv)

- Edit: I found the root cause and will fix it tomorro with the template: 

$ aws --endpoint-url=http://localhost:4566 cloudformation describe-stack-events \
  --stack-name nginx
{
    "StackEvents": [
        {
            "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/nginx/2505d1dc-0d20-4787-a0bd-3bb07b27a28f",
            "EventId": "963fb653-c9c8-4384-9107-257040982139",
            "StackName": "nginx",
            "LogicalResourceId": "nginx",
            "PhysicalResourceId": "arn:aws:cloudformation:us-east-1:000000000000:stack/nginx/2505d1dc-0d20-4787-a0bd-3bb07b27a28f",
            "ResourceType": "AWS::CloudFormation::Stack",
            "Timestamp": "2026-01-21T13:00:18.340239Z",
            "ResourceStatus": "CREATE_FAILED"
        },
        {
            "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/nginx/2505d1dc-0d20-4787-a0bd-3bb07b27a28f",
            "EventId": "3e201a1d-c63f-452e-bd09-8e38183bedd7",
            "StackName": "nginx",
            "LogicalResourceId": "nginx",
            "PhysicalResourceId": "arn:aws:cloudformation:us-east-1:000000000000:stack/nginx/2505d1dc-0d20-4787-a0bd-3bb07b27a28f",
            "ResourceType": "AWS::CloudFormation::Stack",
            "Timestamp": "2026-01-21T13:00:18.340213Z",
            "ResourceStatus": "ROLLBACK_COMPLETE"
        },
        {
            "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/nginx/2505d1dc-0d20-4787-a0bd-3bb07b27a28f",
            "EventId": "9f035218-6b5f-4ee3-aa4e-d27098c4af38",
            "StackName": "nginx",
            "LogicalResourceId": "nginx",
            "PhysicalResourceId": "arn:aws:cloudformation:us-east-1:000000000000:stack/nginx/2505d1dc-0d20-4787-a0bd-3bb07b27a28f",
            "ResourceType": "AWS::CloudFormation::Stack",
            "Timestamp": "2026-01-21T13:00:18.340075Z",
            "ResourceStatus": "CREATE_FAILED"
        },
        {
            "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/nginx/2505d1dc-0d20-4787-a0bd-3bb07b27a28f",
            "EventId": "eafd20af-d4c2-4826-98c3-453bada5f44a",
            "StackName": "nginx",
            "LogicalResourceId": "WebServer",
            "ResourceType": "AWS::EC2::Instance",
            "Timestamp": "2026-01-21T13:00:18.340034Z",
            "ResourceStatus": "CREATE_FAILED",
            "ResourceStatusReason": "Resource provider operation failed: Invalid base64-encoded string: number of data characters (73) cannot be 1 more than a multiple of 4"
        },
        {
            "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/nginx/2505d1dc-0d20-4787-a0bd-3bb07b27a28f",
            "EventId": "ea4ea0fe-8e95-4fc2-8218-d27477e48226",
            "StackName": "nginx",
            "LogicalResourceId": "WebServer",
            "ResourceType": "AWS::EC2::Instance",
            "Timestamp": "2026-01-21T13:00:18.339513Z",
            "ResourceStatus": "CREATE_IN_PROGRESS"
        },
        {
            "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/nginx/2505d1dc-0d20-4787-a0bd-3bb07b27a28f",
            "EventId": "0e61db03-7440-4a63-8776-a6f57e4506d5",
            "StackName": "nginx",
            "LogicalResourceId": "WebSG",
            "PhysicalResourceId": "nginx-WebSG-7239af8b",
            "ResourceType": "AWS::EC2::SecurityGroup",
            "Timestamp": "2026-01-21T13:00:18.339244Z",
            "ResourceStatus": "CREATE_COMPLETE"
        },
        {
            "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/nginx/2505d1dc-0d20-4787-a0bd-3bb07b27a28f",
            "EventId": "b25fa808-d468-4b6c-8516-b0e161b1d264",
            "StackName": "nginx",
            "LogicalResourceId": "WebSG",
            "ResourceType": "AWS::EC2::SecurityGroup",
            "Timestamp": "2026-01-21T13:00:18.324756Z",
            "ResourceStatus": "CREATE_IN_PROGRESS"
        },
        {
            "StackId": "arn:aws:cloudformation:us-east-1:000000000000:stack/nginx/2505d1dc-0d20-4787-a0bd-3bb07b27a28f",
            "EventId": "f2a4deb3-61a0-4f98-a4e5-306f9318fc5c",
            "StackName": "nginx",
            "LogicalResourceId": "nginx",
            "PhysicalResourceId": "arn:aws:cloudformation:us-east-1:000000000000:stack/nginx/2505d1dc-0d20-4787-a0bd-3bb07b27a28f",
            "ResourceType": "AWS::CloudFormation::Stack",
            "Timestamp": "2026-01-21T13:00:18.323812Z",
            "ResourceStatus": "CREATE_IN_PROGRESS"
        }
    ]
}
(.venv)


# 22.1.2026

- Maybe CI/CD for today, we'll see

Installed pylint locally and the plan is to integrate that to the codebase via CI/CD. The linter now runs locally and works.

- Got GitHub Actions CI/CD working and runnign the linter and deployment as expected. Everything works for now.