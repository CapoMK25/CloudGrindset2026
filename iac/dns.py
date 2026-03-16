"""
Route 53 style DNS template for LocalStack deployment.

"""

from troposphere import Template, Ref, ImportValue, Output, Export
from troposphere.route53 import (
    HostedZone, 
    HostedZoneVPCs, 
    HostedZoneConfiguration,
    RecordSet, 
    RecordSetGroup
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

# 2. Add an A-Record (standard practice)
a_record = t.add_resource(
    RecordSetGroup(
        "DnsRecords",
        HostedZoneId=Ref(hosted_zone),
        RecordSets=[
            RecordSet(
                Name=f"map.{DOMAIN_NAME}.",
                Type="A",
                TTL="300",
                ResourceRecords=["10.0.1.10"]
            ),
            RecordSet(
                Name=f"api.{DOMAIN_NAME}.",
                Type="CNAME",
                TTL="300",
                ResourceRecords=[f"map.{DOMAIN_NAME}."]
            )
        ]
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
