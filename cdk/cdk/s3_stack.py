# SPDX-License-Identifier: Apache-2.0
from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_iam as iam,
    RemovalPolicy,
    Duration
)
from constructs import Construct
from .ecs_stack import EcsStack


class S3Stack(Stack):
    def __init__(self, scope: Construct, construct_id: str, ecs_stack: EcsStack, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create S3 bucket with infrequent access
        self.bucket = s3.Bucket(
            self, "OmiBucket",
            bucket_name="omi-data-bucket",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.RETAIN,
            lifecycle_rules=[
                s3.LifecycleRule(
                    transitions=[
                        s3.Transition(
                            storage_class=s3.StorageClass.INFREQUENT_ACCESS,
                            transition_after=Duration.days(30)
                        )
                    ]
                )
            ]
        )

        # Create IAM policy for bucket access
        bucket_policy = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "s3:GetObject",
                "s3:PutObject",
                "s3:ListBucket",
                "s3:DeleteObject"
            ],
            resources=[
                self.bucket.bucket_arn,
                f"{self.bucket.bucket_arn}/*"
            ]
        )

        # Add the S3 policy to both ECS services' task roles
        ecs_stack.backend_service.task_definition.task_role.add_to_policy(bucket_policy)
        ecs_stack.frontend_service.task_definition.task_role.add_to_policy(bucket_policy)
