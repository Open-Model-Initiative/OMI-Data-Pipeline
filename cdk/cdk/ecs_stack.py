# SPDX-License-Identifier: Apache-2.0
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_elasticloadbalancingv2 as elbv2,
    aws_efs as efs,
    aws_iam as iam,
    RemovalPolicy,
)
from constructs import Construct
from .vpc_stack import VpcStack
from .ecr_stack import EcrStack
from .s3_stack import S3Stack


class EcsStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        vpc_stack: VpcStack,
        ecr_stack: EcrStack,
        s3_stack: S3Stack,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create ECS Cluster
        self.cluster = ecs.Cluster(
            self, "OmiCluster", vpc=vpc_stack.vpc, cluster_name="omi-cluster"
        )

        # Security Groups
        backend_sg = ec2.SecurityGroup(
            self,
            "BackendSecurityGroup",
            vpc=vpc_stack.vpc,
            description="Security group for backend service",
            security_group_name="omi-backend-sg",
        )

        frontend_sg = ec2.SecurityGroup(
            self,
            "FrontendSecurityGroup",
            vpc=vpc_stack.vpc,
            description="Security group for frontend service",
            security_group_name="omi-frontend-sg",
        )

        # Create EFS File System
        fs = efs.FileSystem(
            self,
            "OmiFileSystem",
            vpc=vpc_stack.vpc,
            removal_policy=RemovalPolicy.RETAIN,
        )

        # Create EFS Access Point
        access_point = fs.add_access_point(
            "OmiEfsAccessPoint",
            create_acl=efs.Acl(owner_uid="1000", owner_gid="1000", permissions="750"),
            path="/data",
            posix_user=efs.PosixUser(uid="1000", gid="1000"),
        )

        # Create volume configuration
        efs_volume = ecs.Volume(
            name="omi-data-volume",
            efs_volume_configuration=ecs.EfsVolumeConfiguration(
                file_system_id=fs.file_system_id,
                transit_encryption="ENABLED",
                authorization_config=ecs.AuthorizationConfig(
                    access_point_id=access_point.access_point_id, iam="ENABLED"
                ),
            ),
        )

        # Backend Service Task Definition
        task_definition = ecs.FargateTaskDefinition(
            self,
            "OmiBackendTaskDef",
            cpu=256,
            memory_limit_mib=512,
            volumes=[efs_volume],
        )

        # Add S3 permissions to task role
        task_definition.add_to_task_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:ListBucket",
                    "s3:DeleteObject",
                ],
                resources=[
                    s3_stack.bucket.bucket_arn,
                    f"{s3_stack.bucket.bucket_arn}/*",
                ],
            )
        )

        # Add permissions for s3fs-fuse
        task_definition.add_to_task_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "s3:ListAllMyBuckets",
                    "s3:HeadBucket",
                    "s3:ListMultipartUploadParts",
                    "s3:AbortMultipartUpload",
                ],
                resources=["*"],
            )
        )

        container = task_definition.add_container(
            "omi-backend",
            image=ecs.ContainerImage.from_ecr_repository(ecr_stack.backend_repository),
            container_name="omi-backend",
            port_mappings=[ecs.PortMapping(container_port=8000)],
            logging=ecs.LogDriver.aws_logs(stream_prefix="omi-backend"),
            environment={"S3_BUCKET": "omi-data-bucket", "MOUNT_POINT": "/mnt/data"},
            entry_point=["sh", "-c"],
            # todo, move it to a dockerfile
            command=[
                "amazon-linux-extras install -y aws-cli && "
                + "yum install -y s3fs-fuse && "
                + "s3fs $S3_BUCKET $MOUNT_POINT -o iam_role=auto && "
                + "python app.py"
            ],
        )

        container.add_mount_points(
            ecs.MountPoint(
                container_path="/mnt/data",
                source_volume="omi-data-volume",
                read_only=False,
            )
        )

        # Backend Service
        self.backend_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "OmiBackendService",
            cluster=self.cluster,
            task_definition=task_definition,
            desired_count=1,
            public_load_balancer=True,
            security_groups=[backend_sg],
            service_name="omi-backend",
        )

        # Allow EFS access
        fs.connections.allow_default_port_from(self.backend_service.service.connections)

        # Frontend Service Task Definition
        frontend_task_definition = ecs.FargateTaskDefinition(
            self, "OmiFrontendTaskDef", cpu=256, memory_limit_mib=512
        )

        frontend_task_definition.add_container(
            "omi-frontend",
            image=ecs.ContainerImage.from_ecr_repository(ecr_stack.frontend_repository),
            container_name="omi-frontend",
            port_mappings=[ecs.PortMapping(container_port=80)],
            logging=ecs.LogDriver.aws_logs(stream_prefix="omi-frontend"),
        )

        # Frontend Service
        self.frontend_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "OmiFrontendService",
            cluster=self.cluster,
            task_definition=frontend_task_definition,
            desired_count=1,
            public_load_balancer=True,
            security_groups=[frontend_sg],
            service_name="omi-frontend",
        )

        # Allow backend to access database
        backend_sg.add_egress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(5432),
            description="Allow backend to access PostgreSQL",
        )
