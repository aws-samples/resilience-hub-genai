# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0



from aws_cdk import Stack
from aws_cdk import Duration
from aws_cdk import RemovalPolicy
from aws_cdk import aws_s3
from aws_cdk import aws_cloudfront
from aws_cdk import aws_cloudfront_origins
from constructs import Construct
import constants



class CloudFront(Construct):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        assets_bucket = aws_s3.Bucket(
            self,
            id='WebAssets',
            bucket_name=f'{Stack.of(self).account}-genai-resilience-hub-report-assets',
            versioned=False,
            block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,
            enforce_ssl=True,
            auto_delete_objects=True
        )
        self.assets_bucket = assets_bucket

        cache_disabled_policy = aws_cloudfront.CachePolicy(
            self,
            id='CloudFrontCachePolicy',
            cache_policy_name='CloudFrontCachePolicy',
            default_ttl=Duration.seconds(0),
            min_ttl=Duration.seconds(0),
            max_ttl=Duration.seconds(0),
        )
        http_403_error = aws_cloudfront.ErrorResponse(
            http_status=403,
            ttl=Duration.minutes(1),
            response_page_path='/welcome/index.html',
            response_http_status=200
        )
        distribution = aws_cloudfront.Distribution(
            self,
            id='CloudFrontDistribution',
            comment='AWSResilienceHubGenAI',
            default_behavior=aws_cloudfront.BehaviorOptions(
                origin=aws_cloudfront_origins.S3BucketOrigin.with_origin_access_control(assets_bucket),
                cache_policy=cache_disabled_policy,
                viewer_protocol_policy=aws_cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
            ),
            default_root_object="/welcome/index.html",
            error_responses=[http_403_error]
        )

        self.distribution = distribution
