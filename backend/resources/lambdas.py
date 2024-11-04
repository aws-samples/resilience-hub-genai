# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0



from aws_cdk import Stack
from aws_cdk import Duration
from aws_cdk import aws_iam
from aws_cdk import aws_lambda
from constructs import Construct
import constants



class GetApplicationsRole(Construct):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_execution_createlog_statement = aws_iam.PolicyStatement(
                actions=["logs:CreateLogGroup"],
                resources=[f"arn:aws:logs:{Stack.of(self).region}:{Stack.of(self).account}:*"],
        )
        lambda_execution_createstream_statement = aws_iam.PolicyStatement(
            actions=["logs:CreateLogStream", "logs:PutLogEvents"],
            resources=[
                f"arn:aws:logs:{Stack.of(self).region}:{Stack.of(self).account}:log-group:/aws/lambda/GetApplications:*"
            ],
        )
        resilience_hub_statement = aws_iam.PolicyStatement(
            actions=[
                'resiliencehub:ListApps',
                'resiliencehub:ListAppVersions',
                'resiliencehub:ListAppVersionResources',
                'resiliencehub:ListAppAssessments'
            ],
            resources=["*"]
        )
        ssm_statement = aws_iam.PolicyStatement(
            actions=['ssm:GetParameter'],
            resources=[f'arn:aws:ssm:{Stack.of(self).region}:{Stack.of(self).account}:parameter/{constants.SSM_PARAMETER}']
        )

        resilience_hub_get_applications_policy = aws_iam.ManagedPolicy(
            self,
            id='GetApplicationsPolicy',
            managed_policy_name='GetApplicationsPolicy',
            statements=[
                lambda_execution_createlog_statement,
                lambda_execution_createstream_statement,
                resilience_hub_statement,
                ssm_statement
            ]
        )
        resilience_hub_get_applications_role = aws_iam.Role(
            self,
            id='GetApplicationsRole',
            role_name='GetApplicationsRole',
            assumed_by=aws_iam.ServicePrincipal('lambda.amazonaws.com')
        )
        resilience_hub_get_applications_policy.attach_to_role(resilience_hub_get_applications_role)

        self.role = resilience_hub_get_applications_role


class GetApplicationsLambda(Construct):
    def __init__(self, scope: Construct, construct_id: str, role: aws_iam.Role, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        resilience_hub_get_applications_lambda = aws_lambda.Function(
            self,
            id='GetApplications',
            function_name='GetApplications',
            description='Return a list of Applications from Resilience Hub.',
            code=aws_lambda.Code.from_asset('resources/lambda_function_code/get_applications/'),
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            architecture=aws_lambda.Architecture.ARM_64,
            handler='lambda_function.lambda_handler',
            timeout=Duration.seconds(60),
            memory_size=512,
            role=role,
        )

        self.function = resilience_hub_get_applications_lambda


class GenerateReportRole(Construct):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_execution_createlog_statement = aws_iam.PolicyStatement(
                actions=["logs:CreateLogGroup"],
                resources=[f"arn:aws:logs:{Stack.of(self).region}:{Stack.of(self).account}:*"],
        )
        lambda_execution_createstream_statement = aws_iam.PolicyStatement(
            actions=["logs:CreateLogStream", "logs:PutLogEvents"],
            resources=[
                f"arn:aws:logs:{Stack.of(self).region}:{Stack.of(self).account}:log-group:/aws/lambda/GenerateReport:*"
            ],
        )
        bedrock_statement = aws_iam.PolicyStatement(
            actions=["bedrock:InvokeModel"],
            resources=["*"]
        )
        resilience_hub_statement = aws_iam.PolicyStatement(
            actions=[
                'resiliencehub:ListApps',
                'resiliencehub:ListAppVersions',
                'resiliencehub:ListAppVersionResources',
                'resiliencehub:ListAppAssessments',
                'resiliencehub:ListAppComponentRecommendations',
                'resiliencehub:DescribeApp'
            ],
            resources=["*"]
        )
        ssm_statement = aws_iam.PolicyStatement(
            actions=['ssm:GetParameter'],
            resources=[f'arn:aws:ssm:{Stack.of(self).region}:{Stack.of(self).account}:parameter/{constants.SSM_PARAMETER}']
        )

        resilience_hub_generate_report_policy = aws_iam.ManagedPolicy(
            self,
            id='GenerateReportPolicy',
            managed_policy_name='GenerateReportPolicy',
            statements=[
                lambda_execution_createlog_statement,
                lambda_execution_createstream_statement,
                bedrock_statement,
                resilience_hub_statement,
                ssm_statement
            ]
        )
        resilience_hub_generate_report_role = aws_iam.Role(
            self,
            id='GenerateReportRole',
            role_name='GenerateReportRole',
            assumed_by=aws_iam.ServicePrincipal('lambda.amazonaws.com')
        )
        resilience_hub_generate_report_policy.attach_to_role(resilience_hub_generate_report_role)

        self.role = resilience_hub_generate_report_role


class GenerateReportLambda(Construct):
    def __init__(self, scope: Construct, construct_id: str, role: aws_iam.Role, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        resilience_hub_generate_report_lambda = aws_lambda.Function(
            self,
            id='GenerateReport',
            function_name='GenerateReport',
            description='Generate a personalized AWS Resilience Hub report using Amazon Bedrock.',
            code=aws_lambda.Code.from_asset('resources/lambda_function_code/generate_report/'),
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            architecture=aws_lambda.Architecture.ARM_64,
            handler='lambda_function.lambda_handler',
            timeout=Duration.seconds(90),
            memory_size=512,
            role=role,
        )

        self.function = resilience_hub_generate_report_lambda
