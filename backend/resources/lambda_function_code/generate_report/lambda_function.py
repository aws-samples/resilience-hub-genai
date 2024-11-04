# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0


"""
This module provides functionality for generating reports based on Resilience Hub assessments.
"""

import json
from typing import Dict, List
from datetime import datetime
import os
import json
import boto3
import prompts


RH_CLIENT = boto3.client("resiliencehub")
BEDROCK_CLIENT = boto3.client("bedrock-runtime")
MODEL_ID = 'ai21.jamba-1-5-mini-v1:0'


PARAMETERS = os.environ['parameters']

ssm = boto3.client('ssm')
response = ssm.get_parameter(
    Name=PARAMETERS
)
values = json.loads(response['Parameter']['Value'])

ALLOWED_ORIGINS = values['allowed_origins']


def lambda_handler(event: Dict, context) -> Dict:
    """
    Lambda function handler.

    Args:
        event (Dict): Lambda event payload.
        context: Lambda context object.

    Returns:
        Dict: Response payload.
    """
    method = event["httpMethod"]
    path = event["path"]

    if method == "OPTIONS":
        return cors_response(event=event, status_code=200)

    elif method == "POST" and path == "/generate-report":
        request_json = json.loads(event["body"])
        persona = request_json["persona"]
        assessment_arn = request_json["assessment_arn"]
        app_arn = request_json["app_arn"]

        app = describe_app(app_arn)
        app = list_app_version_resources(app)
        app["recommendations"] = get_assessment_recommendations(assessment_arn)
        
        rh_report = build_prompts(app)
        report = str(rh_report)
        prompt = set_prompt(persona, report)
        return cors_response(
            event=event,
            status_code=200,
            body=json.dumps(
                {
                    "generated-text": json.dumps(
                        invoke_jamba_message(BEDROCK_CLIENT, MODEL_ID, prompt)
                    )
                }
            ),
        )
    return cors_response(event=event, status_code=404)


def cors_response(event: Dict, status_code: int, body: str = None) -> Dict:
    """
    Constructs a CORS-enabled response.

    Args:
        evet (dict): lambda event, used to get the origin from headers
        status_code (int): HTTP status code.
        body (str, optional): Response body.

    Returns:
        Dict: Response payload.
    """

    headers = event.get('headers')
    origin = headers.get('origin')

    if origin in ALLOWED_ORIGINS:
        response = {
            "statusCode": status_code,
            "headers": {
                "Access-Control-Allow-Origin": origin,
                "Access-Control-Allow-Methods": "POST",
                "Access-Control-Allow-Headers": "authorization, Content-Type",
            },
        }
        if body:
            response["body"] = body
    else:
        response = {
            "statusCode": 403
        }
    return response


def list_app_versions(client: boto3.Session, apps: List[Dict]) -> List[Dict]:
    """
    Lists the latest version of each application.

    Args:
        client (boto3.Session): Boto3 session.
        apps (List[Dict]): List of application summaries.

    Returns:
        List[Dict]: List of applications with the latest version information.
    """
    for app in apps:
        app_arn = app["appArn"]
        results = get_results(client.list_app_versions, "appVersions", appArn=app_arn)
        app["latestAppVersion"] = results[-1]
        app["latestAppVersion"]["creationTime"] = date_to_string(
            app["latestAppVersion"]["creationTime"]
        )
    return apps


def list_app_version_resources(app: Dict) -> Dict:
    """
    Lists the resources associated with the latest version of an application.

    Args:
        app (Dict): Application details.

    Returns:
        Dict: Application details with resource information.
    """
    app_arn = app["appArn"]
    app_version = "release"
    results = get_results(
        RH_CLIENT.list_app_version_resources,
        "physicalResources",
        appArn=app_arn,
        appVersion=app_version,
    )
    app["resources"] = results
    return app


def list_app_assessments(client: boto3.Session, apps: List[Dict]) -> List[Dict]:
    """
    Lists the latest assessment for each application.

    Args:
        client (boto3.Session): Boto3 session.
        apps (List[Dict]): List of application summaries.

    Returns:
        List[Dict]: List of applications with the latest assessment information.
    """
    for app in apps:
        app_arn = app["appArn"]
        results = get_results(
            client.list_app_assessments, "assessmentSummaries", appArn=app_arn
        )
        latest_assessment = results[-1]
        latest_assessment["endTime"] = date_to_string(latest_assessment["endTime"])
        latest_assessment["startTime"] = date_to_string(latest_assessment["startTime"])
        app["assessment"] = latest_assessment
    return apps


def list_app_component_recommendations(client: boto3.Session, apps: List[Dict]) -> List[Dict]:
    """
    Lists the component recommendations for each application's latest assessment.

    Args:
        client (boto3.Session): Boto3 session.
        apps (List[Dict]): List of application summaries with assessment information.

    Returns:
        List[Dict]: List of applications with component recommendations.
    """
    for app in apps:
        assessment_arn = app["assessment"]["assessmentArn"]
        results = get_results(
            client.list_app_component_recommendations,
            "componentRecommendations",
            assessmentArn=assessment_arn,
        )
        app["recommendations"] = results
    return apps


def build_prompts(app: Dict) -> str:
    """
    Builds a prompt string based on the application details and recommendations.

    Args:
        app (Dict): Application details with recommendations.

    Returns:
        str: Prompt string.
    """
    prompt_strings = []
    prompt_strings.append("```application_details\n")
    prompt_strings.append(f"NAME: {app['name']}\n")
    if 'description' in app:
        prompt_strings.append(f"DESCRIPTION: {app['description']}\n")
    prompt_strings.append(f"COMPLIANCE STATUS: {app['complianceStatus']}\n")
    prompt_strings.append(
        f"LAST ASSESSMENT RUN: {app['lastAppComplianceEvaluationTime']}\n"
    )
    prompt_strings.append(f"RESILIENCY SCORE: int({app['resiliencyScore'] * 100})\n")
    prompt_strings.append("##\n")
    prompt_strings.append("RECOMMENDATIONS:\n")
    for recommendation in app["recommendations"]:
        prompt_strings.append(
            f"{app_component_to_friendly_string(recommendation['appComponentName'], app)}\n"
        )
        prompt_strings.append(
            f"The following recommendation status is {recommendation['recommendationStatus']}\n"
        )
        for configRecommendation in recommendation['configRecommendations']:
            for suggestedChange in configRecommendation['suggestedChanges']:
                prompt_strings.append(
                    f"The following change is suggested {suggestedChange}\n"
                )
    prompt_strings.append("```")
    prompt = "".join(prompt_strings)
    return prompt


def get_results(boto3_method, response_key: str, **kwargs) -> List:
    """
    Retrieves all results from a paginated Boto3 method.

    Args:
        boto3_method: Boto3 method to call.
        response_key (str): Key in the response dictionary containing the results.
        **kwargs: Additional arguments to pass to the Boto3 method.

    Returns:
        List: List of results.
    """
    next_token = None
    processing = True
    results = []
    while processing:
        request = {}
        if next_token is not None:
            request["nextToken"] = next_token
        response = boto3_method(**kwargs)
        results.extend(response[response_key])
        if "nextToken" in response:
            next_token = response["nextToken"]
        else:
            processing = False
    return results


def date_to_string(date: datetime) -> str:
    """
    Converts a datetime object to a string representation.

    Args:
        date (datetime): Datetime object.

    Returns:
        str: String representation of the datetime.
    """
    return date.strftime("%Y-%m-%d %H:%M:%S")


def app_component_to_friendly_string(app_component: str, app: Dict) -> str:
    """
    Constructs a friendly string representation of an application component.

    Args:
        app_component (str): Application component ID.
        app (Dict): Application details.

    Returns:
        str: Friendly string representation of the application component.
    """
    friendly_string = []
    for resource in app["resources"]:
        if resource["appComponents"][0]["id"] == app_component:
            friendly_string.append("Recommendations for ")
            friendly_string.append(resource["physicalResourceId"]["identifier"])
            friendly_string.append(" a ")
            friendly_string.append(resource["resourceType"])
            friendly_string.append(":")
    return "".join(friendly_string)



def set_prompt(persona: str, report: str) -> str:
    prompt = ''
    if persona == "executive":
        prompt = prompts.executive(report)
    elif persona == 'manager':
        prompt = prompts.manager(report)
    elif persona == 'engineer':
        prompt = prompts.engineer(report)
    return prompt


def invoke_jamba_message(client, model_id: str, prompt: str, max_tokens: int = 4000, temperature: float = 0, top_k: int = 1) -> str:
    model_id = MODEL_ID
    body = json.dumps({
        "max_tokens": max_tokens,
        "temperature": temperature,
        "n": 1,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })

    response = ""
    try:
        response = client.invoke_model(
            modelId=model_id,
            body=body
        )

    except Exception as exc:
        result = "Model invocation error"
    try:
        result = json.loads(response.get('body').read())
        text = result['choices'][0]['message']['content']
        return text
    except Exception as exc:
        result = "Output parsing error"
    return result


def get_assessment_recommendations(assessment_arn: str) -> List[Dict]:
    """
    Retrieves the component recommendations for a given assessment.

    Args:
        assessment_arn (str): Assessment ARN.

    Returns:
        List[Dict]: List of component recommendations.
    """
    recommendations = RH_CLIENT.list_app_component_recommendations(
        assessmentArn=assessment_arn
    )
    return recommendations["componentRecommendations"]


def describe_app(app_arn: str) -> Dict:
    """
    Retrieves the details of an application.

    Args:
        app_arn (str): Application ARN.

    Returns:
        Dict: Application details.
    """
    response = RH_CLIENT.describe_app(appArn=app_arn)
    app = response["app"]
    return app


