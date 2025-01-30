# SPDX-License-Identifier: Apache-2.0
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_rds as rds,
    RemovalPolicy
)
from constructs import Construct
from .vpc_stack import VpcStack


class DatabaseStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, vpc_stack: VpcStack, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create database credentials secret
        self.database_secret = rds.DatabaseSecret(
            self, "DatabaseSecret",
            username="postgres",
            secret_name="omi-database-credentials"
        )

        # Security group for RDS
        self.db_security_group = ec2.SecurityGroup(
            self, "DatabaseSecurityGroup",
            vpc=vpc_stack.vpc,
            description="Security group for RDS instance",
            security_group_name="omi-database-sg"
        )

        # Create RDS instance
        self.db_instance = rds.DatabaseInstance(
            self, "Database",
            engine=rds.DatabaseInstanceEngine.postgres(version=rds.PostgresEngineVersion.VER_15),
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MEDIUM),
            vpc=vpc_stack.vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED),
            security_groups=[self.db_security_group],
            credentials=rds.Credentials.from_secret(self.database_secret),
            database_name="omidb",
            port=5432,
            removal_policy=RemovalPolicy.DESTROY,
            deletion_protection=False,
            backup_retention=rds.BackupDuration.days(7),
            instance_identifier="omi-database"
        )
