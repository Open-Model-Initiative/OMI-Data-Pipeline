# SPDX-License-Identifier: Apache-2.0
from aws_cdk import Stack, aws_ec2 as ec2, CfnOutput
from constructs import Construct


class VpcStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create VPC
        self.vpc = ec2.Vpc(
            self,
            "omi-vpc-stack",
            vpc_name="VpcStack",
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            max_azs=2,
            enable_dns_hostnames=True,
            enable_dns_support=True,
            nat_gateways=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24,
                ),
                ec2.SubnetConfiguration(
                    name="Private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24,
                ),
                ec2.SubnetConfiguration(
                    name="Isolated",
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask=24,
                ),
            ]
        )

        # Add VPC Endpoint for Secrets Manager
        self.vpc.add_interface_endpoint(
            "SecretsManagerEndpoint",
            service=ec2.InterfaceVpcEndpointAwsService.SECRETS_MANAGER,
        )

        # Outputs
        CfnOutput(
            self,
            "VpcId",
            value=self.vpc.vpc_id,
            description="ID of the created VPC"
        )
        CfnOutput(
            self,
            "PublicSubnets",
            value=str([subnet.subnet_id for subnet in self.vpc.public_subnets]),
            description="List of public subnet IDs"
        )
        CfnOutput(
            self,
            "PrivateSubnets",
            value=str([subnet.subnet_id for subnet in self.vpc.private_subnets]),
            description="List of private subnet IDs"
        )
        CfnOutput(
            self,
            "DatabaseSubnets",
            value=str([subnet.subnet_id for subnet in self.vpc.isolated_subnets]),
            description="List of isolated subnet IDs for databases"
        )
