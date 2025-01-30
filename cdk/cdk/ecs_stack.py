# SPDX-License-Identifier: Apache-2.0
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_elasticloadbalancingv2 as elbv2
)
from constructs import Construct
from .vpc_stack import VpcStack
from .ecr_stack import EcrStack


class EcsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, vpc_stack: VpcStack, ecr_stack: EcrStack, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create ECS Cluster
        self.cluster = ecs.Cluster(
            self, "OmiCluster",
            vpc=vpc_stack.vpc,
            cluster_name="omi-cluster"
        )

        # Security Groups
        backend_sg = ec2.SecurityGroup(
            self, "BackendSecurityGroup",
            vpc=vpc_stack.vpc,
            description="Security group for backend service",
            security_group_name="omi-backend-sg"
        )

        frontend_sg = ec2.SecurityGroup(
            self, "FrontendSecurityGroup",
            vpc=vpc_stack.vpc,
            description="Security group for frontend service",
            security_group_name="omi-frontend-sg"
        )

        # Backend Service
        self.backend_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "OmiBackendService",
            cluster=self.cluster,
            cpu=256,
            memory_limit_mib=512,
            desired_count=1,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_ecr_repository(ecr_stack.backend_repository),
                container_name="omi-backend",
                container_port=8000,
            ),
            public_load_balancer=True,
            security_groups=[backend_sg],
            service_name="omi-backend"
        )

        # Frontend Service
        self.frontend_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "OmiFrontendService",
            cluster=self.cluster,
            cpu=256,
            memory_limit_mib=512,
            desired_count=1,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_ecr_repository(ecr_stack.frontend_repository),
                container_name="omi-frontend",
                container_port=80,
            ),
            public_load_balancer=True,
            security_groups=[frontend_sg],
            service_name="omi-frontend"
        )

        # Allow backend to access database
        backend_sg.add_egress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(5432),
            description="Allow backend to access PostgreSQL"
        )
