# SPDX-License-Identifier: Apache-2.0
import os

import aws_cdk as cdk

from cdk.cdk_stack import CdkStack
from cdk.vpc_stack import VpcStack
from cdk.database_stack import DatabaseStack
from cdk.ecr_stack import EcrStack
from cdk.ecs_stack import EcsStack
from cdk.s3_stack import S3Stack
from cdk.waf_stack import WafStack


app = cdk.App()
env = cdk.Environment(
    account=os.getenv('CDK_DEFAULT_ACCOUNT'),
    region=os.getenv('CDK_DEFAULT_REGION')
)

vpc_stack = VpcStack(app, "VpcStack", env=env)
database_stack = DatabaseStack(app, "DatabaseStack", vpc_stack=vpc_stack, env=env)
ecr_stack = EcrStack(app, "EcrStack", env=env)
ecs_stack = EcsStack(app, "EcsStack", vpc_stack=vpc_stack, ecr_stack=ecr_stack, env=env)
s3_stack = S3Stack(app, "S3Stack", ecs_stack=ecs_stack, env=env)
waf_stack = WafStack(app, "WafStack", ecs_stack=ecs_stack, env=env)
CdkStack(app, "CdkStack", env=env)

app.synth()
