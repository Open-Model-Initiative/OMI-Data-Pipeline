# SPDX-License-Identifier: Apache-2.0
from aws_cdk import (
    Stack,
    aws_ecr as ecr,
    RemovalPolicy,
    CfnOutput
)
from constructs import Construct


class EcrStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create ECR repository for frontend
        self.frontend_repository = ecr.Repository(
            self, "omi-frontend",
            removal_policy=RemovalPolicy.RETAIN,
            image_scan_on_push=True,
            image_tag_mutability=ecr.TagMutability.MUTABLE,
            lifecycle_rules=[
                ecr.LifecycleRule(
                    max_image_count=10,
                    description="Keep only 10 latest images"
                )
            ]
        )

        # Create ECR repository for backend
        self.backend_repository = ecr.Repository(
            self, "omi-backend",
            removal_policy=RemovalPolicy.RETAIN,
            image_scan_on_push=True,
            image_tag_mutability=ecr.TagMutability.MUTABLE,
            lifecycle_rules=[
                ecr.LifecycleRule(
                    max_image_count=10,
                    description="Keep only 10 latest images"
                )
            ]
        )

        # Outputs
        CfnOutput(self, "FrontendRepositoryUri",
                  value=self.frontend_repository.repository_uri,
                  description="Frontend Repository URI")

        CfnOutput(self, "BackendRepositoryUri",
                  value=self.backend_repository.repository_uri,
                  description="Backend Repository URI")
