"""
EC2 template for LocalStack deployment locally.
Creates an EC2 instance linked to a custom VPC via the Troposphere Python Library.
"""

from troposphere import Template, Ref, Parameter, Base64, ImportValue, Tags, Select, Split, Join
from troposphere.ec2 import Instance, SecurityGroup, SecurityGroupRule
from troposphere.elasticloadbalancingv2 import (
    LoadBalancer, TargetGroup, Listener, Action, TargetDescription
)
t = Template()
t.set_description("Tiered Security: ALB -> EC2 (CloudGrindset 2026)")

# Parameter for instance type
instance_type_param = t.add_parameter(
    Parameter(
        "InstanceType",
        Type="String",
        Description="EC2 Instance Type",
        Default="t3.nano"
    )
)

# ALB Security Group
alb_sg = t.add_resource(
    SecurityGroup(
        "ALBSecurityGroup",
        GroupDescription="Public internet access for the Load Balancer",
        VpcId=ImportValue("GrindsetVPC-ID"),
        SecurityGroupIngress=[
            SecurityGroupRule(
                IpProtocol="tcp",
                FromPort=80,
                ToPort=80,
                CidrIp="0.0.0.0/0",
            )
        ],
        Tags=Tags(Name="ALB-SG")
    )
)

# Web Instance Security Group
web_sg = t.add_resource(
    SecurityGroup(
        "WebServerSG",
        GroupDescription="Allow ONLY ALB and SSH access",
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
                SourceSecurityGroupId=Ref(alb_sg),
            )
        ],
        Tags=Tags(Name="Web-Server-SG")
    )
)

# Define USERDATA_SCRIPT
USERDATA_SCRIPT = '''#!/bin/bash
apt update
apt install -y nginx
systemctl enable nginx
systemctl start nginx
'''

# EC2 Instance itself
web_instance = t.add_resource(
    Instance(
        "WebServerInstance",
        ImageId="ami-fake-local",
        InstanceType=Ref(instance_type_param),
        IamInstanceProfile=ImportValue("iam-stack-InstanceProfileName"),
        SubnetId=ImportValue("GrindsetPublicSubnets-List"),
        SecurityGroupIds=[Ref(web_sg)],
        UserData=Base64(USERDATA_SCRIPT),
        Tags=Tags(Name="Grindset-Web-Server")
    )
)

web_target_group = t.add_resource(
    TargetGroup(
        "WebTargetGroup",
        HealthCheckProtocol="HTTP",
        HealthCheckPort="80",
        HealthCheckPath="/",
        Port=80,
        Protocol="HTTP",
        TargetType="instance",
        Targets=[TargetDescription(Id=Ref(web_instance), Port=80)],
        VpcId=ImportValue("GrindsetVPC-ID"),
    )
)

web_alb = t.add_resource(
    LoadBalancer(
        "ApplicationLoadBalancer",
        Name="Grindset-ALB",
        Scheme="internet-facing",
        Subnets=Split(",", ImportValue("GrindsetPublicSubnets-List")),
        SecurityGroups=[Ref(alb_sg)],
        Tags=Tags(Name="Grindset-ALB")
    )
)

web_listener = t.add_resource(
    Listener(
        "WebListener",
        Port=80,
        Protocol="HTTP",
        LoadBalancerArn=Ref(web_alb),
        DefaultActions=[
            Action(
                Type="forward",
                TargetGroupArn=Ref(web_target_group)
            )
        ]
    )
)

print(t.to_yaml())
