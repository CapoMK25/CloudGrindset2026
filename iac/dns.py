"""
Route 53 style DNS template for LocalStack deployment.
Simplified to avoid resource deployment loops.
"""

from troposphere import Template, Ref, ImportValue, Output, Export
from troposphere.route53 import (
    HostedZone,
    HostedZoneVPCs,
    HostedZoneConfiguration,
    RecordSet
)

t = Template()
t.set_description("DNS for CloudGrindset2026 - Route 53")

# The internal domain
DOMAIN_NAME = "grindset.local"

# 1. Create the Private Hosted Zone
hosted_zone = t.add_resource(
    HostedZone(
        "InternalHostedZone",
        Name=DOMAIN_NAME,
        VPCs=[
            HostedZoneVPCs(
                VPCId=ImportValue("GrindsetVPC-ID"),
                VPCRegion="us-east-1"
            )
        ],
        HostedZoneConfig=HostedZoneConfiguration(
            Comment="DNS (Route53) for the CloudGrindset2026 repo"
        )
    )
)

# 2. Add individual RecordSets instead of a Group to break the loop
t.add_resource(
    RecordSet(
        "MapRecord",
        HostedZoneId=Ref(hosted_zone),
        Name=f"map.{DOMAIN_NAME}.",
        Type="A",
        TTL="300",
        ResourceRecords=["10.0.1.10"]
    )
)

t.add_resource(
    RecordSet(
        "ApiRecord",
        HostedZoneId=Ref(hosted_zone),
        Name=f"api.{DOMAIN_NAME}.",
        Type="CNAME",
        TTL="300",
        ResourceRecords=[f"map.{DOMAIN_NAME}."]
    )
)

# Outputs
t.add_output([
    Output(
        "HostedZoneId",
        Value=Ref(hosted_zone),
        Description="The ID of the Private Hosted Zone",
        Export=Export("GrindsetHostedZone-ID")
    )
])

print(t.to_yaml())
