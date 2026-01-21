from troposphere import Template, Ref, Parameter
from troposphere.ec2 import Instance, SecurityGroup, SecurityGroupRule
from troposphere import Base64

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

# EC2 Instance with Base64 UserData
web_instance = t.add_resource(
    Instance(
        "WebServerInstance",
        ImageId="ami-fake-local",  # LocalStack placeholder AMI
        InstanceType=Ref(instance_type_param),
        SecurityGroups=[Ref(web_sg)],
        UserData=Base64(
            '''#!/bin/bash
apt update
apt install -y nginx
systemctl enable nginx
systemctl start nginx
'''
        )
    )
)

print(t.to_yaml())