# SPDX-License-Identifier: Apache-2.0
from aws_cdk import (
    Duration,
    Stack,
    aws_ec2 as ec2,
    aws_rds as rds,
    RemovalPolicy,
    CfnOutput,
)
from constructs import Construct
from .vpc_stack import VpcStack


class DatabaseStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, vpc_stack: VpcStack, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create database credentials secret
        self.database_secret = rds.DatabaseSecret(
            self,
            "DatabaseSecret",
            username="postgres",
            secret_name="omi-database-credentials",
        )

        # Security group for RDS
        self.db_security_group = ec2.SecurityGroup(
            self,
            "DatabaseSecurityGroup",
            vpc=vpc_stack.vpc,
            description="Security group for RDS instance",
            security_group_name="omi-database-sg",
            allow_all_outbound=False,
        )

        # Allow inbound PostgreSQL traffic from within VPC
        self.db_security_group.add_ingress_rule(
            peer=ec2.Peer.ipv4(vpc_stack.vpc.vpc_cidr_block),
            connection=ec2.Port.tcp(5432),
            description="Allow PostgreSQL access from within VPC",
        )

        self.db_name = "omidb"

        # Create a custom parameter group for PostgreSQL Serverless
        # TODO: Setup certificate for connection to the DB
        self.db_parameter_group = rds.ParameterGroup(
            self,
            "OmiDatabaseParameterGroup",
            engine=rds.DatabaseClusterEngine.aurora_postgres(
                version=rds.AuroraPostgresEngineVersion.Ver
            ),
            description="Parameter group for OMI PostgreSQL Aurora Serverless cluster",
            parameters={
                # Disable SSL requirement
                "rds.force_ssl": "0"
            },
        )

        # Create Aurora Serverless v2 cluster
        self.db_cluster = rds.DatabaseCluster(
            self,
            "DatabaseCluster",
            engine=rds.DatabaseClusterEngine.aurora_postgres(
                version=rds.AuroraPostgresEngineVersion.of(
                    major_version="17",
                    minor_version="5"
                )
            ),
            vpc=vpc_stack.vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            ),
            security_groups=[self.db_security_group],
            credentials=rds.Credentials.from_secret(self.database_secret),
            default_database_name=self.db_name,
            port=5432,
            removal_policy=RemovalPolicy.DESTROY,
            deletion_protection=False,  # set it to true after testing
            cluster_identifier="omi-database-cluster",
            parameter_group=self.db_parameter_group,
            writer=rds.ClusterInstance.provisioned("writer"),
            serverless_v2_min_capacity=0.5,  # Minimum ACUs (Aurora Capacity Units)
            serverless_v2_max_capacity=2,  # Maximum ACUs
        )

        # Output the database endpoint
        CfnOutput(
            self,
            "DatabaseEndpoint",
            value=self.db_cluster.cluster_endpoint.hostname,
            description="Database cluster endpoint address",
        )
