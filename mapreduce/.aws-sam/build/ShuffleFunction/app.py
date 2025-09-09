import os
import json
import boto3

def lambda_handler(event, context):
    lst = event
    benchmark_bucket = lst[0]["benchmark_bucket"]
    bucket = lst[0]["bucket"]
    prefix = lst[0]["prefix"]

    s3 = boto3.client("s3")
    paginator = s3.get_paginator("list_objects_v2")
    page_iter = paginator.paginate(Bucket=benchmark_bucket, Prefix=prefix)
    dirs = []
    for page in page_iter:
        for obj in page.get("Contents", []):
            dirs.append(obj["Key"]) 
    dirs = [p.split(os.sep)[1] for p in dirs]
    dirs = list(set(dirs))
    lst = [{
        "bucket": benchmark_bucket,
        #"dir": os.path.join(bucket, prefix, path)
        #TODO add word here.
        "dir": os.path.join(prefix, path)
        #"dir": os.path.join(bucket, prefix)
    } for path in dirs]


    return lst
