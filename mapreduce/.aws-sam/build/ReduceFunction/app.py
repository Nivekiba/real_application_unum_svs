import os
import io
import json
import boto3

def lambda_handler(event, context):
    bucket = event["bucket"]
    path = event["dir"]

    s3 = boto3.client("s3")
    count = 0
    #each blob is one word.
    paginator = s3.get_paginator("list_objects_v2")
    page_iter = paginator.paginate(Bucket=bucket, Prefix=path)
    for page in page_iter:
        for obj in page.get("Contents", []):
            key = obj["Key"]
            response = s3.get_object(Bucket=bucket, Key=key)
            body = response["Body"].read()
            count += int(body.decode("utf-8"))

    return {
        "word": os.path.basename(path),
        "count": count
    }
