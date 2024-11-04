# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0



import json
from aws_cdk import Stack
from aws_cdk import CfnOutput
from constructs import Construct

from resources.cloudfront import CloudFront
from resources.cognito import Cognito, CreateUser
from resources.lambdas import (
    GetApplicationsRole,
    GetApplicationsLambda,
    GenerateReportRole,
    GenerateReportLambda
)
from resources.apigateway import ApiGateway
from resources.parameter import Parameter
import constants



class AppStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, description: str = constants.STACK_DESCRIPTION, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        cloudfront = CloudFront(
            self, 
            'WebSite',
        )

        cognito = Cognito(
            self, 
            'Authentication'
        )

        get_applications_role = GetApplicationsRole(
            self,
            'GetApplicationsRole'
        )

        get_applications_lambda = GetApplicationsLambda(
            self,
            'GetApplicationsLambda',
            get_applications_role.role
        )

        generate_report_role = GenerateReportRole(
            self,
            'GenerateReportRole'

        )

        generate_report_lambda = GenerateReportLambda(
            self,
            'GenerateReportLambda',
            generate_report_role.role
        )


        api_gateway = ApiGateway(
            self,
            'ResilienceHubReportApi',
            get_applications_function=get_applications_lambda.function,
            generate_report_function = generate_report_lambda.function,
            user_pool=cognito.user_pool
        )

        allowed_origins = f'https://{api_gateway.api.url}, https://{cloudfront.distribution.domain_name}'

        parameter_name = constants.SSM_PARAMETER
        parameter_value = json.dumps({
            'allowed_origins': allowed_origins,
            'user_pool_id': cognito.user_pool.user_pool_id,
            'user_email': constants.EMAIL
        })

        parameters = Parameter(
            self,
            'Parameter',
            parameter_name,
            parameter_value
        )

        get_applications_lambda.function.add_environment(
            key='parameters',
            value=parameter_name
        )

        generate_report_lambda.function.add_environment(    
            key='parameters',
            value=parameter_name
        )

        create_user = CreateUser(self, 'create-user', cognito.user_pool)

        create_user.function.add_environment(
            key='parameters',
            value=parameter_name
        )


        CfnOutput(
            self,
            "REGION",
            value=Stack.of(self).region
        )

        CfnOutput(
            self,
            "S3_ASSET_BUCKET",
            value=cloudfront.assets_bucket.bucket_name
        )

        CfnOutput(
            self,
            "CLOUDFRONT_DISTRIBUTION",
            value=cloudfront.distribution.distribution_domain_name
        )

        CfnOutput(
            self,
            "COGNITO_USERPOOL_ID",
            value=cognito.user_pool.user_pool_id
        )

        CfnOutput(
            self,
            "COGNITO_USERPOOL_CLIENT_ID",
            value=cognito.user_pool_client.user_pool_client_id
        )

        CfnOutput(
            self,
            'API_GATEWAY_URL',
            value=api_gateway.api.url
        )

        CfnOutput(
            self,
            'API_GATEWAY_GET_APPLICATIONS_OPTIONS_PATH',
            value=api_gateway.paths['get-applications-options']
        )

        CfnOutput(
            self,
            'API_GATEWAY_GENERATE_REPORT_PATH',
            value=api_gateway.paths['generate-report']
        )

        CfnOutput(
            self,
            'SIGNON_EMAIL',
            value=constants.EMAIL
        )
