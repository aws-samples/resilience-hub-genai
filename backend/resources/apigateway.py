
from aws_cdk import Duration
from aws_cdk import aws_apigateway
from aws_cdk import aws_cognito
from aws_cdk import aws_lambda
from constructs import Construct
import constants



class ApiGateway(Construct):
    def __init__(self, scope: Construct, construct_id: str, get_applications_function: aws_lambda.Function, generate_report_function: aws_lambda.Function, user_pool: aws_cognito.UserPool, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        rest_api = aws_apigateway.RestApi(
            self,
            id='ResilienceHubReportAPI',
            endpoint_types=[aws_apigateway.EndpointType.REGIONAL],
            deploy_options=aws_apigateway.StageOptions(
                metrics_enabled=True,
                logging_level=aws_apigateway.MethodLoggingLevel.INFO,
                data_trace_enabled=False,
                stage_name='live'
            ),
            
            deploy=True
        )

        authorizer = aws_apigateway.CognitoUserPoolsAuthorizer(
            self,
            id='Authorizer',
            authorizer_name='Authorizer',
            cognito_user_pools=[user_pool]
        )


        get_applications_options = rest_api.root.add_resource('get-applications-options')
        get_applications_options.add_method(
            http_method='OPTIONS',
            integration=aws_apigateway.LambdaIntegration(
                handler=get_applications_function,
                proxy=True,
                timeout=Duration.seconds(5)
            ),
        )

        get_applications_options.add_method(
            http_method='GET',
            authorizer=authorizer,
            integration=aws_apigateway.LambdaIntegration(
                handler=get_applications_function,
                proxy=True,
                timeout=Duration.seconds(25)
            ),
        )

        generate_report = rest_api.root.add_resource('generate-report')
        generate_report.add_method(
            http_method='OPTIONS',
            integration=aws_apigateway.LambdaIntegration(
                handler=generate_report_function,
                proxy=True,
                timeout=Duration.seconds(5)
            ),
        )

        generate_report.add_method(
            http_method='POST',
            authorizer=authorizer,
            integration=aws_apigateway.LambdaIntegration(
                handler=generate_report_function,
                proxy=True,
                timeout=Duration.seconds(25)
            ),
        )

        self.api = rest_api
        self.paths = {
            'get-applications-options': get_applications_options.path,
            'generate-report': generate_report.path
        }
