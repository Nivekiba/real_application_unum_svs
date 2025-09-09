import os
import io
import uuid
import boto3

def chunks(lst, n):
    m = int(len(lst) / n)
    for i in range(n-1):
        yield lst[i*m:i*m+m]
    tail = lst[(n-1)*m:]
    if len(tail) > 0:
        yield tail

def lambda_handler(event, context):
    benchmark_bucket = event["benchmark_bucket"]
    words_bucket = event["words_bucket"]
    words_blob = event["words"]
    words_path = os.path.join("/tmp", "words.txt")

    s3 = boto3.client("s3")
    # s3.download_file(benchmark_bucket, words_bucket + '/' + words_blob, words_path)
    s3.download_file(words_bucket, words_blob, words_path)
    with open(words_path, "r") as f:
        list = f.read().split("\n")
    os.remove(words_path)

    n_mappers = event["n_mappers"]
    output_bucket = event["output_bucket"]
    map_lists = chunks(list, n_mappers)
    blobs = []

    
    for chunk in map_lists:
        name = str(uuid.uuid4())[:8]
        data = io.BytesIO()
        data.writelines((val+"\n").encode("utf-8") for val in chunk)
        data.seek(0)

        key = output_bucket + '/' + name
        s3.put_object(Bucket=benchmark_bucket, Key=key, Body=data.getvalue())
        stripped_name = name
        blobs.append(stripped_name)

    prefix = str(uuid.uuid4())[:8]
    lst = [{
        "benchmark_bucket": benchmark_bucket,
        "bucket": output_bucket,
        "blob": b,
        "prefix": prefix
    } for b in blobs]

    # return {
    #     "list": lst
    # }
    return lst
