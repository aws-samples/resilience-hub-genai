import json
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

import boto3
import os
import json

RESILIENCEHUB_CLIENT = boto3.client("resiliencehub")

PARAMETERS = os.environ['parameters']

ssm = boto3.client('ssm')
response = ssm.get_parameter(
    Name=PARAMETERS
)
values = json.loads(response['Parameter']['Value'])

ALLOWED_ORIGINS = values['allowed_origins']

class HttpMethods(str, Enum):
    """
    HTTP methods supported by the Lambda function.
    """

    GET = "GET"
    OPTIONS = "OPTIONS"


class Paths(str, Enum):
    """
    Paths supported by the Lambda function.
    """

    GET_APPLICATIONS_OPTIONS = "/get-applications-options"


@dataclass
class Response:
    """
    Response object for the Lambda function.
    """

    status_code: int
    headers: Dict[str, str]
    body: Optional[str] = None

    def to_dict(self) -> Dict:
        """
        Convert the Response object to a dictionary.
        """
        return {
            "statusCode": self.status_code,
            "headers": self.headers,
            "body": self.body,
        }


def lambda_handler(event, context) -> Response:
    """
    Lambda function handler.

    Args:
        event: Event object received from AWS Lambda.
        context: Context object received from AWS Lambda.

    Returns:
        Response object containing the response for the API Gateway.
    """
    http_method = HttpMethods(event["httpMethod"])
    path = Paths(event["path"])
    headers = event.get('headers')
    origin = headers.get('origin')
        

    if http_method == HttpMethods.OPTIONS:
        if origin in ALLOWED_ORIGINS:
            response = Response(
                status_code=200,
                headers={
                    "Access-Control-Allow-Origin": origin,
                    "Access-Control-Allow-Methods": "GET, POST",
                    "Access-Control-Allow-Headers": "authorization, Content-Type",
                },
            )
        else:
            response = Response(
                status_code=403,
                headers={}
            )
        
    elif http_method == HttpMethods.GET and path == Paths.GET_APPLICATIONS_OPTIONS:
        assessment_options = get_assessment_options()
        response_body = json.dumps(assessment_options)
        if origin in ALLOWED_ORIGINS:
            response = Response(
                status_code=200,
                headers={
                    "Access-Control-Allow-Origin": origin,
                    "Content-Type": "application/json",
                },
                body=response_body,
            )
        else:
            response = Response(
                status_code=403
            )
        
    else:
        response = Response(
        status_code=403,
        body="Invalid Request",
    )
    return response.to_dict()


def get_assessment_options() -> List[Dict]:
    """
    Build and return the list of assessments for the Web UI.

    Returns:
        List of dictionaries containing the application name, application ARN, and assessment ARN.
    """
    active_apps = list_active_apps(client=RESILIENCEHUB_CLIENT)

    release_apps = list_release_versions(client=RESILIENCEHUB_CLIENT, apps=active_apps)

    app_assessments = list_latest_app_assessments(
        client=RESILIENCEHUB_CLIENT, apps=release_apps
    )

    options = build_app_assessment_list(
        client=RESILIENCEHUB_CLIENT,
        assessments=app_assessments,
        apps=release_apps,
    )
    return options


def list_active_apps(client: boto3.Session) -> List[Dict]:
    """
    List your Resilience Hub applications and filter out the inactive ones.

    Args:
        client: Boto3 client for Resilience Hub.

    Returns:
        List of dictionaries representing active Resilience Hub applications.
    """
    app_summaries = []
    response = client.list_apps()
    app_summaries += response["appSummaries"]

    while "nextToken" in response:
        next_token = response["nextToken"]
        response = client.list_apps(nextToken=next_token)
        app_summaries += response["appSummaries"]

    active_apps = [app for app in app_summaries if app["status"] == "Active"]
    return active_apps


def list_release_versions(client: boto3.Session, apps: List[Dict]) -> List[Dict]:
    """
    List the release versions for the given Resilience Hub applications.

    Args:
        client: Boto3 client for Resilience Hub.
        apps: List of dictionaries representing Resilience Hub applications.

    Returns:
        List of dictionaries representing Resilience Hub applications with a release version.
    """
    release_apps = []
    for app in apps:
        app_versions = []
        app_arn = app["appArn"]
        response = client.list_app_versions(appArn=app_arn)
        app_versions += response["appVersions"]

        while "nextToken" in response:
            next_token = response["nextToken"]
            response = client.list_app_versions(appArn=app_arn, nextToken=next_token)
            app_versions += response["appVersions"]

        if any(version["appVersion"] == "release" for version in app_versions):
            release_apps.append(app)

    return release_apps


def list_latest_app_assessments(client: boto3.Session, apps: List[Dict]) -> List[Dict]:
    """
    List the latest successful assessment for the given Resilience Hub applications.

    Args:
        client: Boto3 client for Resilience Hub.
        apps: List of dictionaries representing Resilience Hub applications.

    Returns:
        List of dictionaries representing the latest successful assessment for each application.
    """
    latest_app_assessments = []
    for app in apps:
        assessment_summaries = []
        app_arn = app["appArn"]
        response = client.list_app_assessments(appArn=app_arn)
        assessment_summaries += response["assessmentSummaries"]

        while "nextToken" in response:
            next_token = response["nextToken"]
            response = client.list_app_assessments(appArn=app_arn, nextToken=next_token)
            assessment_summaries += response["assessmentSummaries"]

        successful_assessment_summaries = [
            assesment
            for assesment in assessment_summaries
            if assesment["assessmentStatus"] == "Success"
        ]
        sorted_assessment_summaries = sorted(
            successful_assessment_summaries, key=lambda x: x["endTime"], reverse=True
        )

        if sorted_assessment_summaries:
            latest_app_assessments.append(sorted_assessment_summaries[0])

    return latest_app_assessments


def build_app_assessment_list(
    client: boto3.Session, assessments: List[Dict], apps: List[Dict]
) -> List[Dict]:
    """
    Build a list of application name, application ARN, and assessment ARN pairs.

    Args:
        client: Boto3 client for Resilience Hub.
        assessments: List of dictionaries representing assessments.
        apps: List of dictionaries representing applications.

    Returns:
        List of dictionaries containing the application name, application ARN, and assessment ARN.
    """
    app_assessment_list = []
    for assessment in assessments:
        app_arn = assessment["appArn"]
        for app in apps:
            if app_arn == app["appArn"]:
                app_assessment_list.append(
                    {
                        "app_name": app["name"],
                        "app_arn": app["appArn"],
                        "assessment_arn": assessment["assessmentArn"],
                    }
                )

    return app_assessment_list
