from troposphere import Template, Ref, Parameter, Output
import troposphere.ec2 as ec2

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
sg = t.add_resource(ec2.SecurityGroup(
    "WebSG",
    GroupDescription="Allow HTTP/SSH",
    SecurityGroupIngress=[
        ec2.SecurityGroupRule(IpProtocol="tcp", FromPort=22, ToPort=22, CidrIp="0.0.0.0/0"),
        ec2.SecurityGroupRule(IpProtocol="tcp", FromPort=80, ToPort=80, CidrIp="0.0.0.0/0"),
    ]
))

# 4️⃣ EC2 Instance (simulated)
userdata_script = """#!/bin/bash
apt update
apt install -y nginx
systemctl enable nginx
systemctl start nginx
"""

instance = t.add_resource(ec2.Instance(
    "WebServer",
    InstanceType=Ref(instance_type_param),
    ImageId="ami-fake-local",  # placeholder since we’re not deploying to AWS
    SecurityGroups=[Ref(sg)],
    UserData=userdata_script
))

# 5️⃣ Output
t.add_output([
    Output("InstanceId", Value=Ref(instance), Description="EC2 Instance ID")
])

# 6️⃣ Print YAML
print(t.to_yaml())
