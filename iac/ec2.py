"""
EC2 template for LocalStack deployment locally.
Creates an EC2 instance for LocalStack via the Troposphere Python Library.
"""

from troposphere import Template, Ref, Parameter, Base64
from troposphere.ec2 import Instance, SecurityGroup, SecurityGroupRule


t = Template()
t.set_description("Baseline EC2 Linux setup for LocalStack testing")

# Parameter for instance type
instance_type_param = t.add_parameter(
    Parameter(
        "InstanceType",
        Type="String",
        Description="EC2 Instance Type",
        Default="t3.nano"
    )
)

# Security Group
web_sg = t.add_resource(
    SecurityGroup(
        "WebServerSG",
        GroupDescription="Allow HTTP and SSH access",
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

# Define USERDATA_SCRIPT here
USERDATA_SCRIPT = '''#!/bin/bash
apt update
apt install -y nginx
systemctl enable nginx
systemctl start nginx
'''

# EC2 Instance
web_instance = t.add_resource(
    Instance(
        "WebServerInstance",
        ImageId="ami-fake-local",  # LocalStack placeholder, not a real AMI
        InstanceType=Ref(instance_type_param),
        SecurityGroups=[Ref(web_sg)],
        UserData=Base64(USERDATA_SCRIPT)
    )
)

print(t.to_yaml())
