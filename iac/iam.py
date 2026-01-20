from troposphere import Template
from troposphere.iam import (
    User,
    Group,
    PolicyType,
    ManagedPolicy,
    UserToGroupAddition
)

t = Template()
t.set_description("Baseline IAM setup for LocalStack for myself")

# IAM Group
admins_group = t.add_resource(
    Group(
        "AdminsGroup",
        GroupName="Admins"
    )
)

# IAM User
mk_user = t.add_resource(
    User(
        "MKUser",
        UserName="MK"
    )
)

# Attach AWS managed AdministratorAccess policy (the default)
admin_policy = t.add_resource(
    ManagedPolicy(
        "AdminsManagedPolicy",
        ManagedPolicyName="AdminsAdministratorAccess",
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
        Groups=["Admins"]
    )
)

# Add user to group
t.add_resource(
    UserToGroupAddition(
        "AddMKToAdmins",
        GroupName="Admins",
        Users=["MK"]
    )
)

print(t.to_yaml())
