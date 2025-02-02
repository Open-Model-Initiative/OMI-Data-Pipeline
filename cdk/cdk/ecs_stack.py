# SPDX-License-Identifier: Apache-2.0
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_elasticloadbalancingv2 as elbv2,
    aws_efs as efs,
    aws_iam as iam,
    aws_secretsmanager as secretsmanager,
    RemovalPolicy,
    Environment,
)
from constructs import Construct
from .vpc_stack import VpcStack
from .ecr_stack import EcrStack
from .s3_stack import S3Stack
from .database_stack import DatabaseStack


class EcsStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        vpc_stack: VpcStack,
        ecr_stack: EcrStack,
        s3_stack: S3Stack,
        database_stack: DatabaseStack,
        env: Environment,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        region = env.region
        account = env.account

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
            path="/upload",
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

        s3_policy = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "s3:GetObject",
                "s3:PutObject",
                "s3:ListBucket",
                "s3:DeleteObject",
            ],
            resources=[s3_stack.bucket.bucket_arn, f"{s3_stack.bucket.bucket_arn}/*"],
        )

        default_policy = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "logs:CreateLogGroup",
                "elasticfilesystem:ClientMount",
                "elasticfilesystem:ClientWrite",
                "elasticfilesystem:ClientRootAccess",
                "elasticfilesystem:DescribeMountTargets",
                "elasticfilesystem:DescribeFileSystems",
                "secretsmanager:GetSecretValue",
            ],
            resources=["*"],
        )

        default_environment = {
            "ROOT_DIR": ".",
            "MODEL_CACHE_DIR": "/mnt/models",
            "S3_BUCKET": s3_stack.bucket.bucket_name,
            "UPLOAD_DIR": "/mnt/upload",
            "POSTGRES_HOST": database_stack.db_instance.db_instance_endpoint_address,
            "POSTGRES_PORT": database_stack.db_instance.db_instance_endpoint_port,
            "POSTGRES_DB": database_stack.db_name,
        }

        omi_sercret_arn = (
            f"arn:aws:secretsmanager:{region}:{account}:secret:omi-oauth2-i1xzfK"
        )

        default_secrets = {
            "POSTGRES_USER": ecs.Secret.from_secrets_manager(
                secret=database_stack.database_secret, field="username"
            ),
            "POSTGRES_PASSWORD": ecs.Secret.from_secrets_manager(
                secret=database_stack.database_secret, field="password"
            ),
            "GOOGLE_CLIENT_ID": ecs.Secret.from_secrets_manager(
                secret=secretsmanager.Secret.from_secret_complete_arn(
                    self,
                    "google-oauth2-id",
                    secret_complete_arn=omi_sercret_arn,
                ),
                field="google_client_id",
            ),
            "GOOGLE_CLIENT_SECRET": ecs.Secret.from_secrets_manager(
                secret=secretsmanager.Secret.from_secret_complete_arn(
                    self,
                    "google-oauth2-secret",
                    secret_complete_arn=omi_sercret_arn,
                ),
                field="google_client_secret",
            ),
            "GITHUB_CLIENT_ID": ecs.Secret.from_secrets_manager(
                secret=secretsmanager.Secret.from_secret_complete_arn(
                    self,
                    "github-oauth2-id",
                    secret_complete_arn=omi_sercret_arn,
                ),
                field="github_client_id",
            ),
            "GITHUB_CLIENT_SECRET": ecs.Secret.from_secrets_manager(
                secret=secretsmanager.Secret.from_secret_complete_arn(
                    self,
                    "github-oauth2-secret",
                    secret_complete_arn=omi_sercret_arn,
                ),
                field="github_client_secret",
            ),
            "DISCORD_CLIENT_ID": ecs.Secret.from_secrets_manager(
                secret=secretsmanager.Secret.from_secret_complete_arn(
                    self,
                    "discord-oauth2-id",
                    secret_complete_arn=omi_sercret_arn,
                ),
                field="discord_client_id",
            ),
            "DISCORD_CLIENT_SECRET": ecs.Secret.from_secrets_manager(
                secret=secretsmanager.Secret.from_secret_complete_arn(
                    self,
                    "discord-oauth2-secret",
                    secret_complete_arn=omi_sercret_arn,
                ),
                field="discord_client_secret",
            ),
        }

        # Backend Service Task Definition
        backend_task_definition = ecs.FargateTaskDefinition(
            self,
            "OmiBackendTaskDef",
            cpu=512,
            memory_limit_mib=1024,
            volumes=[efs_volume],
        )

        # Add S3 permissions to task role
        backend_task_definition.add_to_task_role_policy(s3_policy)

        # Add permissions for mounting EFS and accessing secrets
        backend_task_definition.add_to_task_role_policy(default_policy)

        backend_container = backend_task_definition.add_container(
            "omi-backend",
            image=ecs.ContainerImage.from_ecr_repository(ecr_stack.backend_repository),
            container_name="omi-backend",
            port_mappings=[ecs.PortMapping(container_port=8000)],
            logging=ecs.LogDriver.aws_logs(stream_prefix="omi-backend"),
            environment=default_environment,
            secrets=default_secrets,
            # test which is better, mount point or s3fs command
            # entry_point=["sh", "-c"],
            # command=[
            #     + "s3fs $S3_BUCKET $UPLOAD_DIR -o iam_role=auto && "
            #     + "uvicorn odr_api.app:app --host 0.0.0.0 --port 31100 --reload"
            # ]
        )

        backend_container.add_mount_points(
            ecs.MountPoint(
                container_path="/mnt/upload",
                source_volume="omi-data-volume",
                read_only=False,
            )
        )

        # Backend Service
        self.backend_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "OmiBackendService",
            cluster=self.cluster,
            task_definition=backend_task_definition,
            desired_count=1,
            public_load_balancer=False,
            security_groups=[backend_sg],
            service_name="omi-backend",
        )

        # Allow EFS access
        fs.connections.allow_default_port_from(self.backend_service.service.connections)

        # Frontend Service Task Definition
        frontend_task_definition = ecs.FargateTaskDefinition(
            self,
            "OmiFrontendTaskDef",
            cpu=256,
            memory_limit_mib=512,
            volumes=[efs_volume],
        )

        # Add S3 permissions to task role
        frontend_task_definition.add_to_task_role_policy(s3_policy)

        # Add permissions for mounting EFS and accessing secrets
        frontend_task_definition.add_to_task_role_policy(default_policy)

        frontend_container = frontend_task_definition.add_container(
            "omi-frontend",
            image=ecs.ContainerImage.from_ecr_repository(ecr_stack.frontend_repository),
            container_name="omi-frontend",
            port_mappings=[ecs.PortMapping(container_port=80)],
            logging=ecs.LogDriver.aws_logs(stream_prefix="omi-frontend"),
            environment=default_environment
            | {
                "API_SERVICE_URL": f"http://{self.backend_service.load_balancer.load_balancer_dns_name}"
            },
            secrets=default_secrets,
            # test which is better, mount point or s3fs command
            # entry_point=["sh", "-c"],
            # command=[
            #     + "s3fs $S3_BUCKET $UPLOAD_DIR -o iam_role=auto && "
            #     + "/entrypoint.sh pnpm run dev -- --host 0.0.0.0"
            # ]
        )

        frontend_container.add_mount_points(
            ecs.MountPoint(
                container_path="/mnt/upload",
                source_volume="omi-data-volume",
                read_only=False,
            )
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

        # Allow frontend to access backend
        backend_sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(8000),
            description="Allow frontend to access backend",
        )

        # Allow frontend to database
        frontend_sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(5432),
            description="Allow frontend to access PostgreSQL",
        )
