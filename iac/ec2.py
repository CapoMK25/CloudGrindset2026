"""
Secure EC2: Restricted Ingress (Checkov Compliant)
"""
from troposphere import Template, Ref, Parameter, Base64, ImportValue, Tags, Split, Select
from troposphere.ec2 import Instance, SecurityGroup, SecurityGroupRule

t = Template()
t.set_description("Secure EC2: Restricted Ingress for CloudGrindset2026")

instance_type_param = t.add_parameter(
    Parameter(
        "InstanceType",
        Type="String",
        Default="t3.nano"
    )
)

# 1. Restricted Security Group
web_sg = t.add_resource(
    SecurityGroup(
        "WebServerSG",
        GroupDescription="Allow HTTP access ONLY from within the VPC",
        VpcId=ImportValue("GrindsetVPC-ID"),
        SecurityGroupIngress=[
            SecurityGroupRule(
                Description="Allow HTTP traffic from the VPC only",
                IpProtocol="tcp",
                FromPort=80,
                ToPort=80,
                CidrIp=ImportValue("GrindsetVPC-CIDR")
            )
        ],
        Tags=Tags(Name="Web-Server-SG")
    )
)

# 2. Web Server Instance
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
