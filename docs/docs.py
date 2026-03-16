"""Module to generate architecture diagrams."""
# pylint: disable=expression-not-assigned, pointless-statement, missing-final-newline

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.network import Route53
from diagrams.aws.storage import S3
from diagrams.aws.database import Dynamodb
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM

with Diagram("CloudGrindset 2026 Stack",
            show=False,
            filename="assets/architecture",
            direction="TB"):

    dns = Route53("map.grindset.local")

    with Cluster("LocalStack Environment"):
        with Cluster("VPC (10.0.0.0/16)"):

            with Cluster("Public Network"):
                web_server = EC2("Web Server")
                s3_web = S3("Website Bucket")

            with Cluster("Private Data Layer"):
                db = Dynamodb("User Data")

        iam = IAM("Instance Profiles")
        monitor = Cloudwatch("Health Metrics")

    # Output connections
    dns >> Edge(label="Resolves to") >> web_server
    web_server >> Edge(label="Syncs") >> s3_web
    web_server >> Edge(label="Queries") >> db
    monitor >> Edge(style="dotted") >> web_server
    web_server - iam