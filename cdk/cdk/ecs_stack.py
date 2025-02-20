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
    CfnOutput,
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
            actions=["logs:CreateLogGroup"],
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
            "DEFAULT_SUPERUSER_EMAIL": "opendatarepository@opendatarepository.com",
            "DEFAULT_SUPERUSER_PASSWORD": "",
            "DEFAULT_SUPERUSER_USERNAME": "opendatarepository",
            "TEST_POSTGRES_DB": "",
            "AWS_S3_ENABLED": "true",
        }

        omi_sercret_arn = (
            "arn:aws:secretsmanager:us-east-1:474668405283:secret:omi-oauth2-i1xzfK"
        )

        hf_sercret_arn = (
            "arn:aws:secretsmanager:us-east-1:474668405283:secret:huggingface-0L3S0w"
        )

        default_secrets = {
            "HF_TOKEN": ecs.Secret.from_secrets_manager(
                secret=secretsmanager.Secret.from_secret_complete_arn(
                    self,
                    "hf-token",
                    secret_complete_arn=hf_sercret_arn,
                ),
                field="token",
            ),
            "HF_HDR_DATASET_NAME": ecs.Secret.from_secrets_manager(
                secret=secretsmanager.Secret.from_secret_complete_arn(
                    self,
                    "hf-hdr-dataset-name",
                    secret_complete_arn=hf_sercret_arn,
                ),
                field="hdr_dataset_name",
            ),
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
            "OmiBackendTaskDefiniton",
            cpu=1024,
            memory_limit_mib=2048,
        )

        # Add S3 permissions to task role
        backend_task_definition.add_to_task_role_policy(s3_policy)

        # Add permissions for mounting EFS and accessing secrets
        backend_task_definition.add_to_task_role_policy(default_policy)

        backend_task_definition.add_container(
            "omi-backend",
            image=ecs.ContainerImage.from_ecr_repository(ecr_stack.backend_repository),
            container_name="omi-backend",
            port_mappings=[ecs.PortMapping(container_port=31100)],
            logging=ecs.LogDriver.aws_logs(stream_prefix="omi-backend"),
            environment=default_environment,
            secrets=default_secrets,
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
            "OmiFrontendTaskDefiniton",
            cpu=1024,
            memory_limit_mib=2048,
        )

        # Add S3 permissions to task role
        frontend_task_definition.add_to_task_role_policy(s3_policy)

        # Add permissions for mounting EFS and accessing secrets
        frontend_task_definition.add_to_task_role_policy(default_policy)

        frontend_container = frontend_task_definition.add_container(
            "omi-frontend",
            image=ecs.ContainerImage.from_ecr_repository(ecr_stack.frontend_repository),
            container_name="omi-frontend",
            port_mappings=[ecs.PortMapping(container_port=5173)],
            logging=ecs.LogDriver.aws_logs(stream_prefix="omi-frontend"),
            environment=default_environment
            | {
                "API_SERVICE_URL": f"http://{self.backend_service.load_balancer.load_balancer_dns_name}:31100",
            },
            secrets=default_secrets,
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

        frontend_container.add_environment(
            "AWS_HOSTNAME", self.frontend_service.load_balancer.load_balancer_dns_name
        )

        # Backend security group rules
        # Allow inbound traffic only from frontend security group on backend port
        backend_sg.add_ingress_rule(
            peer=frontend_sg,
            connection=ec2.Port.tcp(31100),
            description="Allow frontend to backend traffic",
        )

        # Backend security group rules - only necessary egress rules
        backend_sg.add_egress_rule(
            peer=database_stack.db_security_group,
            connection=ec2.Port.tcp(5432),
            description="Allow backend to RDS",
        )

        # Frontend security group rules
        # Allow inbound HTTP/HTTPS traffic from anywhere
        frontend_sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(80),
            description="Allow HTTP inbound",
        )
        frontend_sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(443),
            description="Allow HTTPS inbound",
        )

        # Allow frontend to RDS communication
        frontend_sg.add_egress_rule(
            peer=database_stack.db_security_group,
            connection=ec2.Port.tcp(5432),
            description="Allow frontend to RDS",
        )

        # Allow outbound traffic to backend and for HTTPS
        frontend_sg.add_egress_rule(
            peer=backend_sg,
            connection=ec2.Port.tcp(31100),
            description="Allow frontend to backend traffic",
        )
        frontend_sg.add_egress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(443),
            description="Allow HTTPS outbound for external calls",
        )

        # Outputs
        CfnOutput(
            self,
            "ClusterName",
            value=self.cluster.cluster_name,
            description="Name of the created ECS cluster",
        )
        CfnOutput(
            self,
            "BackendServiceUrl",
            value=f"http://{self.backend_service.load_balancer.load_balancer_dns_name}",
            description="URL of the backend service",
        )
        CfnOutput(
            self,
            "FrontendServiceUrl",
            value=f"http://{self.frontend_service.load_balancer.load_balancer_dns_name}",
            description="URL of the frontend service",
        )
