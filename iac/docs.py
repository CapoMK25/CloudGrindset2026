"""Module to generate architecture diagrams."""
# pylint: disable=expression-not-assigned, pointless-statement, missing-final-newline

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.network import ALB
from diagrams.aws.security import IAMRole
from diagrams.aws.storage import S3
from diagrams.aws.management import Cloudwatch

with Diagram("CloudGrindset Architecture",
            show=False,
            filename="assets/architecture",
            direction="LR"):

    with Cluster("Local Emulated Cloud (LocalStack)"):
        bucket = S3("regional-map-2024-website")
        monitor = Cloudwatch("4xx Error Alarm")
        monitor >> Edge(color="firebrick", style="dashed", label="monitors") >> bucket

    with Cluster("AWS Cloud"):
        iam = IAMRole("Instance Profile")
        logs = S3("ALB Access Logs")

        with Cluster("VPC"):
            with Cluster("Public Subnets"):
                lb = ALB("Web ALB")
                server = EC2("Web Server")

                # Logical Flow
                lb >> Edge(label="port 80") >> server
                server - iam
                lb - logs
