"""
NGINX machine template for LocalStack deployment locally.
Creates an NGINX instance for LocalStack via the Troposphere Python Library.
"""

from troposphere import Template, Ref, Parameter, Output, Base64
from troposphere.ec2 import SecurityGroup, SecurityGroupRule, Instance


# This is just a troposphere demonstration for now without deployment running on Localstack

# 1️⃣ Create template
t = Template()
t.set_description("Local NGINX server simulation for static site without AWS on Localstack")

# 2️⃣ Parameters (optional)
instance_type_param = t.add_parameter(Parameter(
    "InstanceType",
    Type="String",
    Default="t3.nano",  # just for simulation purposes
    Description="Instance type"
))

# 3️⃣ Security Group (simulation)
sg = t.add_resource(SecurityGroup(
    "WebSG",
    GroupDescription="Allow HTTP/SSH",
    SecurityGroupIngress=[
        SecurityGroupRule(IpProtocol="tcp", FromPort=22, ToPort=22, CidrIp="0.0.0.0/0"),
        SecurityGroupRule(IpProtocol="tcp", FromPort=80, ToPort=80, CidrIp="0.0.0.0/0"),
    ]
))

# 4️⃣ NGINX Instance (simulated)
USERDATA_SCRIPT = """#!/bin/bash
apt update
apt install -y nginx
systemctl enable nginx
systemctl start nginx
"""

instance = t.add_resource(Instance(
    "WebServer",
    InstanceType=Ref(instance_type_param),
    ImageId="ami-fake-local",  # placeholder since we’re not deploying to AWS
    SecurityGroups=[Ref(sg)],
    UserData=Base64(USERDATA_SCRIPT)
))

# 5️⃣ Output
t.add_output([
    Output("InstanceId", Value=Ref(instance), Description="EC2 Instance ID")
])

# 6️⃣ Print YAML
print(t.to_yaml())
