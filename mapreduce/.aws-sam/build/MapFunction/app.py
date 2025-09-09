import os
import io
import boto3


def count_words(lst):
    index = dict()
    for word in lst:
        if len(word) == 0:
            continue

        val = index.get(word, 0)
        index[word] = val + 1

    return index

def lambda_handler(event, context):
    benchmark_bucket = event["benchmark_bucket"]
    bucket = event["bucket"]
    blob = event["blob"]
    prefix = event["prefix"]

    s3 = boto3.client("s3")
    obj = s3.get_object(Bucket=benchmark_bucket, Key=bucket + '/' + blob)
    body = obj["Body"].read()
    words = body.decode("utf-8").split("\n")
 
    index = count_words(words)
    for word, count in index.items():
        data = io.BytesIO()
        data.write(str(count).encode("utf-8"))
        data.seek(0)
        
        key = os.path.join(prefix, word, blob)
        s3.put_object(Bucket=benchmark_bucket, Key=key, Body=data.getvalue())

    return event
