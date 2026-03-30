"""
This module defines the EC2 instances and related security groups 
for the LocalStack deployment using Troposphere.
"""

from troposphere import (
    Template, Ref,
    Parameter, Base64,
    ImportValue, Tags,
    Split, Select
)
from troposphere.ec2 import Instance, SecurityGroup, SecurityGroupRule
from troposphere.elasticloadbalancingv2 import (
    LoadBalancer, LoadBalancerAttributes,
    TargetGroup, Listener,
    Action, TargetDescription
)

t = Template()
t.set_description("Tiered Security: ALB -> EC2 (CloudGrindset 2026)")

instance_type_param = t.add_parameter(
    Parameter(
        "InstanceType",
        Type="String",
        Default="t3.nano"
    )
)

# 1. ALB Security Group
alb_sg = t.add_resource(
    SecurityGroup(
        "ALBSecurityGroup",
        GroupDescription="Public internet access for the Load Balancer",
        VpcId=ImportValue("GrindsetVPC-ID"),
        SecurityGroupIngress=[
            SecurityGroupRule(
                Description="Allow HTTP from the Internet",
                IpProtocol="tcp",
                FromPort=80,
                ToPort=80,
                CidrIp="0.0.0.0/0"
            )
        ],
        Tags=Tags(Name="ALB-SG"),
        Metadata={
            "checkov": {
                "skip": [
                    {
                        "id": "CKV_AWS_260",
                        "comment": "ALB must be open on port 80 for public web traffic."
                    }
                ]
            }
        }
    )
)

# 2. Web Server Security Group
web_sg = t.add_resource(
    SecurityGroup(
        "WebServerSG",
        GroupDescription="Allow ONLY ALB access",
        VpcId=ImportValue("GrindsetVPC-ID"),
        SecurityGroupIngress=[
            SecurityGroupRule(
                Description="Allow HTTP traffic from ALB SG only",
                IpProtocol="tcp",
                FromPort=80,
                ToPort=80,
                SourceSecurityGroupId=Ref(alb_sg)
            )
        ],
        Tags=Tags(Name="Web-Server-SG")
    )
)

# 3. Instance
web_instance = t.add_resource(
    Instance(
        "WebServerInstance",
        ImageId="ami-fake-local",
        InstanceType=Ref(instance_type_param),
        IamInstanceProfile=ImportValue("iam-stack-InstanceProfileName"),
        SubnetId=Select(0, Split(",", ImportValue("GrindsetPublicSubnets-List"))),
        SecurityGroupIds=[Ref(web_sg)],
        UserData=Base64("#!/bin/bash\napt update\napt install -y nginx\nsystemctl start nginx\n"),
        Tags=Tags(Name="Grindset-Web-Server")
    )
)

# --- TARGET GROUP (Optimized for speed/LocalStack) ---
web_target_group = t.add_resource(
    TargetGroup(
        "WebTargetGroup",
        Port=80,
        Protocol="HTTP",
        TargetType="instance",
        Targets=[TargetDescription(Id=Ref(web_instance), Port=80)],
        VpcId=ImportValue("GrindsetVPC-ID"),
        # NEW: Fast Fail/Fast Success health checks to prevent CloudFormation hanging
        HealthCheckProtocol="HTTP",
        HealthCheckPort="80",
        HealthCheckPath="/",
        HealthyThresholdCount=2,  # Minimum possible
        UnhealthyThresholdCount=2,  # Minimum possible
        HealthCheckTimeoutSeconds=5,
        HealthCheckIntervalSeconds=10, 
    )
)

# 4. Load Balancer
web_alb = t.add_resource(
    LoadBalancer(
        "WebLoadBalancer",
        Name="Grindset-Web-ALB",
        Scheme="internet-facing",
        Subnets=Split(",", ImportValue("GrindsetPublicSubnets-List")),
        SecurityGroups=[Ref(alb_sg)],
        LoadBalancerAttributes=[
            LoadBalancerAttributes(
                Key="access_logs.s3.enabled",
                Value="true"),
            LoadBalancerAttributes(
                Key="access_logs.s3.bucket",
                Value=ImportValue("Grindset-ALB-Log-Bucket")),
            LoadBalancerAttributes(
                Key="routing.http.drop_invalid_header_fields.enabled",
                Value="true")
        ],
        Tags=Tags(Name="Grindset-Web-ALB")
    )
)

# 5. Listener
web_listener = t.add_resource(
    Listener(
        "WebListener",
        Port=80,
        Protocol="HTTP",
        LoadBalancerArn=Ref(web_alb),
        DefaultActions=[Action(Type="forward", TargetGroupArn=Ref(web_target_group))],
        # Explicitly wait for the Target Group to be fully defined
        DependsOn=["WebLoadBalancer", "WebTargetGroup"],
        Metadata={
            "checkov": {
                "skip": [
                    {
                        "id": "CKV_AWS_2",
                        "comment": "Using HTTP for localstack/demo purposes without ACM cert."
                    },
                    {
                        "id": "CKV_AWS_103",
                        "comment": "TLS 1.2 not applicable for HTTP listener."
                    }
                ]
            }
        }
    )
)

print(t.to_yaml())
