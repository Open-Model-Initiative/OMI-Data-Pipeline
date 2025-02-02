# SPDX-License-Identifier: Apache-2.0
from aws_cdk import Stack, aws_s3 as s3, aws_iam as iam, RemovalPolicy, Duration
from constructs import Construct


class S3Stack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create S3 bucket with infrequent access
        self.bucket = s3.Bucket(
            self,
            "OmiBucket",
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
                            transition_after=Duration.days(30),
                        )
                    ]
                )
            ],
        )
