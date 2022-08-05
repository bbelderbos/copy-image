import logging
import os

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from django.conf import settings

DEFAULT_ACL = "private"
SIGN_REQUEST_EXPIRATION = 3600


def create_presigned_url(
    object_name, expiration=SIGN_REQUEST_EXPIRATION, bucket=None
):
    """
    Generate a presigned URL to share an S3 object
    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html
    """
    if bucket is None:
        bucket = settings.AWS_S3_BUCKET

    # Generate a presigned URL for the S3 object
    config = Config(
        region_name=settings.AWS_REGION,
        signature_version="s3v4",
        s3={"addressing_style": "virtual"},
    )
    s3_client = boto3.client("s3", config=config)
    try:
        logging.info(f"{bucket=}, {object_name=}")
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": object_name},
            ExpiresIn=expiration,
        )
    except ClientError as e:
        logging.error(e)
        return None

    return url


def upload_to_s3(file, acl=DEFAULT_ACL, bucket=None, region=None):
    if bucket is None:
        bucket = settings.AWS_S3_BUCKET

    if region is None:
        region = settings.AWS_REGION

    config = Config(region_name=region)
    s3 = boto3.resource("s3", config=config)
    response = s3.Bucket(bucket).put_object(
        Key=file.name,
        Body=file.file,
        ACL=acl
    )

    url = f"https://{bucket}.s3.{region}.amazonaws.com/{response.key}"
    return url

