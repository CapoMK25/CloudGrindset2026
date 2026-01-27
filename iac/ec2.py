"""
EC2 template for LocalStack deployment locally.
Creates an EC2 instance linked to a custom VPC via the Troposphere Python Library.
"""

from troposphere import Template, Ref, Parameter, Base64, ImportValue
from troposphere.ec2 import Instance, SecurityGroup, SecurityGroupRule

t = Template()
t.set_description("EC2 Linux setup integrated with a Custom Networking Stack")

# Parameter for instance type
instance_type_param = t.add_parameter(
    Parameter(
        "InstanceType",
        Type="String",
        Description="EC2 Instance Type",
        Default="t3.nano"
    )
)

# 1. Security Group - Linked to the custom VPC via an ImportValue
web_sg = t.add_resource(
    SecurityGroup(
        "WebServerSG",
        GroupDescription="Allow HTTP and SSH access",
        VpcId=ImportValue("GrindsetVPC-ID"),
        SecurityGroupIngress=[
            SecurityGroupRule(
                IpProtocol="tcp",
                FromPort=22,
                ToPort=22,
                CidrIp="0.0.0.0/0"
            ),
            SecurityGroupRule(
                IpProtocol="tcp",
                FromPort=80,
                ToPort=80,
                CidrIp="0.0.0.0/0"
            )
        ]
    )
)

# Define USERDATA_SCRIPT
USERDATA_SCRIPT = '''#!/bin/bash
apt update
apt install -y nginx
systemctl enable nginx
systemctl start nginx
'''

# 2. EC2 Instance - Using NetworkInterface to specify Subnet and SG
web_instance = t.add_resource(
    Instance(
        "WebServerInstance",
        ImageId="ami-fake-local",
        InstanceType=Ref(instance_type_param),
        SubnetId=ImportValue("GrindsetPublicSubnet-ID"),
        SecurityGroupIds=[Ref(web_sg)],
        UserData=Base64(USERDATA_SCRIPT)
    )
)

print(t.to_yaml())
