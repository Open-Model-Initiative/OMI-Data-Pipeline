# SPDX-License-Identifier: Apache-2.0
from aws_cdk import Duration, Stack, aws_ec2 as ec2, aws_rds as rds, RemovalPolicy
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

        # Create RDS instance
        self.db_instance = rds.DatabaseInstance(
            self,
            "Database",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_17_2
            ),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO
            ),
            vpc=vpc_stack.vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            ),
            security_groups=[self.db_security_group],
            credentials=rds.Credentials.from_secret(self.database_secret),
            database_name=self.db_name,
            port=5432,
            removal_policy=RemovalPolicy.DESTROY,
            deletion_protection=False,  # set it to true after testing
            backup_retention=Duration.days(7),
            instance_identifier="omi-database",
            multi_az=False,
        )
