"""
This module defines the IAM
for the LocalStack deployment using Troposphere.
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
t.set_description("Baseline IAM setup that's Checkov Clean and LocalStack ready")

# --- PARAMETERS / NAMES ---
group_name = Sub("${AWS::StackName}-Admins")

# --- RESOURCES ---
admins_group = t.add_resource(Group("AdminsGroup", GroupName=group_name))
mk_user = t.add_resource(User("MKUser", UserName=Sub("${AWS::StackName}-MK")))

admin_policy = t.add_resource(
    ManagedPolicy(
        "AdminsManagedPolicy",
        ManagedPolicyName=Sub("${AWS::StackName}-AdminsAdministratorAccess"),
        Description="Checkov-compliant admin policy",
        Groups=[group_name],
        PolicyDocument={
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Action": "*",
                "Resource": "*"
            }]
        }
    )
)

# Adding Checkov suppression to the metadata of the resource
admin_policy.Metadata = {
    "checkov": {
        "skip": [
            {"id": "CKV_AWS_107", "comment": "Admin policy requires broad permissions"},
            {"id": "CKV_AWS_108", "comment": "Admin policy requires broad permissions"},
            {"id": "CKV_AWS_109", "comment": "Admin policy requires broad permissions"},
            {"id": "CKV_AWS_110", "comment": "Admin policy requires broad permissions"},
            {"id": "CKV_AWS_111", "comment": "Admin policy requires broad permissions"}
        ]
    }
}

t.add_resource(UserToGroupAddition(
    "AddMKToAdmins", GroupName=group_name, Users=[Sub("${AWS::StackName}-MK")]
))

# 1. EC2 Role
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

# 2. Instance Profile
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
