# SPDX-License-Identifier: Apache-2.0
from aws_cdk import (
    Stack,
    aws_wafv2 as wafv2
)
from constructs import Construct
from .ecs_stack import EcsStack


class WafStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, ecs_stack: EcsStack, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create WAF ACL
        self.waf_acl = wafv2.CfnWebACL(
            self, "OmiWafAcl",
            default_action=wafv2.CfnWebACL.DefaultActionProperty(allow={}),
            scope="REGIONAL",
            visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                cloud_watch_metrics_enabled=True,
                metric_name="OmiWafMetrics",
                sampled_requests_enabled=True
            ),
            rules=[
                # Rate limiting rule
                wafv2.CfnWebACL.RuleProperty(
                    name="RateLimit",
                    priority=1,
                    statement=wafv2.CfnWebACL.StatementProperty(
                        rate_based_statement=wafv2.CfnWebACL.RateBasedStatementProperty(
                            limit=2000,
                            aggregate_key_type="IP"
                        )
                    ),
                    action=wafv2.CfnWebACL.RuleActionProperty(block={}),
                    visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                        cloud_watch_metrics_enabled=True,
                        metric_name="RateLimitRule",
                        sampled_requests_enabled=True
                    )
                ),
                # SQL injection protection
                wafv2.CfnWebACL.RuleProperty(
                    name="SQLInjectionProtection",
                    priority=2,
                    override_action=wafv2.CfnWebACL.OverrideActionProperty(none={}),
                    statement=wafv2.CfnWebACL.StatementProperty(
                        managed_rule_group_statement=wafv2.CfnWebACL.ManagedRuleGroupStatementProperty(
                            name="AWSManagedRulesSQLiRuleSet",
                            vendor_name="AWS"
                        )
                    ),
                    visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                        cloud_watch_metrics_enabled=True,
                        metric_name="SQLInjectionProtectionRule",
                        sampled_requests_enabled=True
                    )
                ),
                # Common vulnerabilities protection
                wafv2.CfnWebACL.RuleProperty(
                    name="CommonVulnerabilities",
                    priority=3,
                    override_action=wafv2.CfnWebACL.OverrideActionProperty(none={}),
                    statement=wafv2.CfnWebACL.StatementProperty(
                        managed_rule_group_statement=wafv2.CfnWebACL.ManagedRuleGroupStatementProperty(
                            name="AWSManagedRulesCommonRuleSet",
                            vendor_name="AWS"
                        )
                    ),
                    visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                        cloud_watch_metrics_enabled=True,
                        metric_name="CommonVulnerabilitiesRule",
                        sampled_requests_enabled=True
                    )
                )
            ]
        )

        # Associate WAF with ALBs
        wafv2.CfnWebACLAssociation(
            self, "BackendWafAssociation",
            resource_arn=ecs_stack.backend_service.load_balancer.load_balancer_arn,
            web_acl_arn=self.waf_acl.attr_arn
        )

        wafv2.CfnWebACLAssociation(
            self, "FrontendWafAssociation",
            resource_arn=ecs_stack.frontend_service.load_balancer.load_balancer_arn,
            web_acl_arn=self.waf_acl.attr_arn
        )
