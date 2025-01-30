# SPDX-License-Identifier: Apache-2.0
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    CfnOutput
)
from constructs import Construct


class VpcStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create VPC
        self.vpc = ec2.Vpc(
            self,
            "omi-vpc-stack",
            vpc_name="VpcStack",
            ip_addresses=ec2.IpAddresses.cidr("10.1.0.0/16"),
            max_azs=1,
            enable_dns_hostnames=True,
            enable_dns_support=True,
            # Subnet configuration
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="database",
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask=24
                )
            ],
            nat_gateways=1
        )

        # Add VPC Endpoint for Secrets Manager
        self.vpc.add_interface_endpoint(
            "SecretsManagerEndpoint",
            service=ec2.InterfaceVpcEndpointAwsService.SECRETS_MANAGER
        )

        # Outputs
        CfnOutput(self, "VpcId", value=self.vpc.vpc_id)
        CfnOutput(self, "PublicSubnets", value=str([subnet.subnet_id for subnet in self.vpc.public_subnets]))
        CfnOutput(self, "PrivateSubnets", value=str([subnet.subnet_id for subnet in self.vpc.private_subnets]))
        CfnOutput(self, "DatabaseSubnets", value=str([subnet.subnet_id for subnet in self.vpc.isolated_subnets]))
