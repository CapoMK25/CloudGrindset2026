from troposphere import Template, Sub
from troposphere.iam import (
    User,
    Group,
    ManagedPolicy,
    UserToGroupAddition
)

t = Template()
t.set_description("Baseline IAM setup for LocalStack for myself")

group_name = Sub("${AWS::StackName}-Admins")

# IAM Group
admins_group = t.add_resource(
    Group(
        "AdminsGroup",
        GroupName=group_name
    )
)

# IAM User
mk_user = t.add_resource(
    User(
        "MKUser",
        UserName=Sub("${AWS::StackName}-MK")
    )
)

# Managed Policy
admin_policy = t.add_resource(
    ManagedPolicy(
        "AdminsManagedPolicy",
        ManagedPolicyName=Sub("${AWS::StackName}-AdminsAdministratorAccess"),
        PolicyDocument={
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": "*",
                    "Resource": "*"
                }
            ]
        },
        Groups=[group_name]
    )
)

# Add user to group
t.add_resource(
    UserToGroupAddition(
        "AddMKToAdmins",
        GroupName=group_name,
        Users=[Sub("${AWS::StackName}-MK")]
    )
)

print(t.to_yaml())
