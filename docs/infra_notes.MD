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