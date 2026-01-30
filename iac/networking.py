"""
Networking template for LocalStack deployment.
Refactored for Multi-AZ High Availability.
"""

from troposphere import Template, Ref, Output, Export, Tags, Join
from troposphere.ec2 import (
    VPC, Subnet, InternetGateway,
    VPCGatewayAttachment, RouteTable, Route,
    SubnetRouteTableAssociation
)

t = Template()
t.set_description("Multi-AZ Networking Layer for CloudGrindset2026")

AZS = ["us-east-1a", "us-east-1b"]
PUBLIC_CIDRS = ["10.0.1.0/24", "10.0.2.0/24"]
PRIVATE_CIDRS = ["10.0.10.0/24", "10.0.11.0/24"]

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

# 2. Internet Gateway
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

# 4. Route Table for Public Subnets (One table for all public AZs)
public_route_table = t.add_resource(
    RouteTable(
        "PublicRouteTable",
        VpcId=Ref(main_vpc),
        Tags=Tags(Name="Public-RT")
    )
)

# 5. Default Route to Internet
t.add_resource(
    Route(
        "PublicRoute",
        DependsOn="VPCGatewayAttachment",
        GatewayId=Ref(igw),
        DestinationCidrBlock="0.0.0.0/0",
        RouteTableId=Ref(public_route_table),
    )
)

# --- DYNAMIC MULTI-AZ GENERATION ---
public_subnet_refs = []
private_subnet_refs = []

for i, az in enumerate(AZS):
    # Public Subnets
    pub_sn = t.add_resource(
        Subnet(
            f"PublicSubnetAZ{i+1}",
            VpcId=Ref(main_vpc),
            CidrBlock=PUBLIC_CIDRS[i],
            MapPublicIpOnLaunch=True,
            AvailabilityZone=az,
            Tags=Tags(Name=f"Public-Subnet-{az}")
        )
    )
    public_subnet_refs.append(Ref(pub_sn))

    t.add_resource(
        SubnetRouteTableAssociation(
            f"PublicAssocAZ{i+1}",
            SubnetId=Ref(pub_sn),
            RouteTableId=Ref(public_route_table),
        )
    )

    # Private Subnets
    priv_sn = t.add_resource(
        Subnet(
            f"PrivateSubnetAZ{i+1}",
            VpcId=Ref(main_vpc),
            CidrBlock=PRIVATE_CIDRS[i],
            AvailabilityZone=az,
            Tags=Tags(Name=f"Private-Subnet-{az}")
        )
    )
    private_subnet_refs.append(Ref(priv_sn))

# --- Outputs ---
t.add_output([
    Output(
        "VpcId",
        Description="The ID of the VPC",
        Value=Ref(main_vpc),
        Export=Export("GrindsetVPC-ID")
    ),
    Output(
        "PublicSubnetIds",
        Description="List of Public Subnet IDs",
        Value=Join(",", public_subnet_refs),
        Export=Export("GrindsetPublicSubnets-List")
    ),
    Output(
        "PrivateSubnetIds",
        Description="List of Private Subnet IDs",
        Value=Join(",", private_subnet_refs),
        Export=Export("GrindsetPrivateSubnets-List")
    )
])

print(t.to_yaml())
