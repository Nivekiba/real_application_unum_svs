import os
import io
import uuid
import json
import sys


def lambda_handler(event, context):
    # previous handler(event) logic preserved
    frames = event

    logs = {}
    for xs in frames:
      for key,value in xs.items():
        logs[key] = value

    return logs
