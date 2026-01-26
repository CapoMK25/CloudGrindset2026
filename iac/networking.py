"""
Networking template for LocalStack deployment.
Creates a custom VPC, Subnets, and Routing infrastructure via Troposphere.
"""

from troposphere import Template, Ref, Output, Export, Tags
from troposphere.ec2 import (
    VPC, Subnet, InternetGateway,
    VPCGatewayAttachment, RouteTable, Route,
    SubnetRouteTableAssociation
)

t = Template()
t.set_description("Custom VPC Networking Layer for CloudGrindset2026")

# 1. Create the VPC
main_vpc = t.add_resource(
    VPC(
        "MainVPC",
        CidrBlock="10.0.0.0/16",
        EnableDnsSupport=True,
        EnableDnsHostnames=True,
        Tags=Tags(Name="Grindset-VPC")
    )
)

# 2. Internet Gateway (Required for Public Internet Access)
igw = t.add_resource(
    InternetGateway(
        "InternetGateway",
        Tags=Tags(Name="Grindset-IGW")
    )
)

# 3. Attach Gateway to VPC
t.add_resource(
    VPCGatewayAttachment(
        "VPCGatewayAttachment",
        VpcId=Ref(main_vpc),
        InternetGatewayId=Ref(igw)
    )
)

# 4. Public Subnet
public_subnet = t.add_resource(
    Subnet(
        "PublicSubnet",
        VpcId=Ref(main_vpc),
        CidrBlock="10.0.1.0/24",
        MapPublicIpOnLaunch=True,
        AvailabilityZone="us-east-1a",
        Tags=Tags(Name="Public-Subnet-Web")
    )
)

# 5. Route Table for Public Subnet
public_route_table = t.add_resource(
    RouteTable(
        "PublicRouteTable",
        VpcId=Ref(main_vpc),
        Tags=Tags(Name="Public-RT")
    )
)

# 6. Default Route to Internet (0.0.0.0/0) via IGW
t.add_resource(
    Route(
        "PublicRoute",
        DependsOn="VPCGatewayAttachment",
        GatewayId=Ref(igw),
        DestinationCidrBlock="0.0.0.0/0",
        RouteTableId=Ref(public_route_table),
    )
)

# 7. Associate Public Subnet with Route Table
t.add_resource(
    SubnetRouteTableAssociation(
        "PublicSubnetRouteTableAssociation",
        SubnetId=Ref(public_subnet),
        RouteTableId=Ref(public_route_table),
    )
)

# 8. Private Subnet (Isolated, no route to IGW)
private_subnet = t.add_resource(
    Subnet(
        "PrivateSubnet",
        VpcId=Ref(main_vpc),
        CidrBlock="10.0.2.0/24",
        AvailabilityZone="us-east-1b",
        Tags=Tags(Name="Private-Subnet-DB")
    )
)

# --- Outputs for Cross-Stack Referencing ---
# This allows other stacks (like EC2) to know where to deploy.

t.add_output([
    Output(
        "VpcId",
        Description="The ID of the VPC",
        Value=Ref(main_vpc),
        Export=Export("GrindsetVPC-ID")
    ),
    Output(
        "PublicSubnetId",
        Description="The ID of the Public Subnet",
        Value=Ref(public_subnet),
        Export=Export("GrindsetPublicSubnet-ID")
    )
])

print(t.to_yaml())
