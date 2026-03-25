"""
Simplified EC2 for LocalStack Community Tier
Removes ALB components to prevent resource deployment loops.
"""
from troposphere import Template, Ref, Parameter, Base64, ImportValue, Tags, Split, Select
from troposphere.ec2 import Instance, SecurityGroup, SecurityGroupRule

t = Template()
t.set_description("Simplified EC2: Direct Access (LocalStack Compatible)")

instance_type_param = t.add_parameter(
    Parameter(
        "InstanceType",
        Type="String",
        Default="t3.nano"
    )
)

# 1. Simplified Security Group (Direct HTTP Access)
web_sg = t.add_resource(
    SecurityGroup(
        "WebServerSG",
        GroupDescription="Allow Direct HTTP access for LocalStack testing",
        VpcId=ImportValue("GrindsetVPC-ID"),
        SecurityGroupIngress=[
            SecurityGroupRule(
                Description="Allow HTTP traffic from anywhere",
                IpProtocol="tcp",
                FromPort=80,
                ToPort=80,
                CidrIp="0.0.0.0/0"
            )
        ],
        Tags=Tags(Name="Web-Server-SG")
    )
)

# 2. Web Server Instance
# Fixed IamInstanceProfile to match the actual export name 'iam-InstanceProfileName'
web_instance = t.add_resource(
    Instance(
        "WebServerInstance",
        ImageId="ami-fake-local",
        InstanceType=Ref(instance_type_param),
        IamInstanceProfile=ImportValue("iam-InstanceProfileName"),
        SubnetId=Select(0, Split(",", ImportValue("GrindsetPublicSubnets-List"))),
        SecurityGroupIds=[Ref(web_sg)],
        UserData=Base64("#!/bin/bash\napt update\napt install -y nginx\n"),
        Tags=Tags(Name="Grindset-Web-Server")
    )
)

print(t.to_yaml())
