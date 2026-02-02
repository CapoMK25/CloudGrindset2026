"""
IAM template for LocalStack deployment locally.
Creates Users, Groups, and Policies via the Troposphere Python Library.
"""

from troposphere import Template, Sub, Export, Output, Ref
from troposphere.iam import (
    User,
    Group,
    ManagedPolicy,
    UserToGroupAddition,
    Role,
    InstanceProfile,
    Policy
)

t = Template()
t.set_description("Baseline IAM setup with an EC2 Role for LocalStack")

group_name = Sub("${AWS::StackName}-Admins")

# --- EXISTING STACKS ---
admins_group = t.add_resource(Group("AdminsGroup", GroupName=group_name))
mk_user = t.add_resource(User("MKUser", UserName=Sub("${AWS::StackName}-MK")))

admin_policy = t.add_resource(
    ManagedPolicy(
        "AdminsManagedPolicy",
        ManagedPolicyName=Sub("${AWS::StackName}-AdminsAdministratorAccess"),
        PolicyDocument={
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow", 
                "Action": [
                    "ec2:*",
                    "s3:*",
                    "iam:*",
                    "cloudwatch:*",
                    "vpc*",
                    "dynamodb*"
                ], 
                "Resource": "*",
                "Condition": {
                "Bool": {"aws:MultiFactorAuthPresent": "true"}
                }
            }]
        },
        Groups=[group_name]
    )
)

t.add_resource(UserToGroupAddition(
    "AddMKToAdmins", GroupName=group_name, Users=[Sub("${AWS::StackName}-MK")]
))

# 1. What the EC2 is allowed to do
web_server_role = t.add_resource(
    Role(
        "WebServerRole",
        RoleName=Sub("${AWS::StackName}-WebServerRole"),
        AssumeRolePolicyDocument={
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Principal": {"Service": ["ec2.amazonaws.com"]},
                "Action": ["sts:AssumeRole"]
            }]
        },
        # Allow Read Access to S3
        Policies=[
            Policy(
                PolicyName="S3ReadAccess",
                PolicyDocument={
                    "Version": "2012-10-17",
                    "Statement": [{
                        "Effect": "Allow",
                        "Action": ["s3:Get*", "s3:List*"],
                        "Resource": [
                            "arn:aws:s3:::regional-map-2024-website",
                            "arn:aws:s3:::regional-map-2024-website/*"
                        ]
                    }]
                }
            )
        ]
    )
)

# 2. The Instance Profile
web_server_profile = t.add_resource(
    InstanceProfile(
        "WebServerInstanceProfile",
        InstanceProfileName=Sub("${AWS::StackName}-EC2-Profile"),
        Roles=[Ref(web_server_role)]
    )
)

# 3. Export
t.add_output(Output(
    "WebServerInstanceProfileName",
    Value=Ref(web_server_profile),
    Export=Export(Sub("${AWS::StackName}-InstanceProfileName"))
))

print(t.to_yaml())
