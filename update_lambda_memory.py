#!/usr/bin/env python3
"""
Modify memory settings for AWS Lambda functions listed in a file.

Each line in the input file must be in the form:
functionName: functionArn

Example:
mapFunction: arn:aws:lambda:us-east-1:123456789012:function:my-map
reduceFunction: arn:aws:lambda:us-east-1:123456789012:function:my-reduce
"""

import argparse
import sys
import re
from typing import Tuple, Optional, List

try:
    import boto3
    from botocore.config import Config
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    print("boto3 is required. Install with: pip install boto3", file=sys.stderr)
    sys.exit(1)


def parse_line(line: str, line_number: int) -> Optional[Tuple[str, str]]:
    # Strip comments and whitespace; ignore blank lines
    cleaned = re.sub(r"#.*$", "", line).strip()
    if not cleaned:
        return None

    # Expect "name: arn..." with at least one colon
    if ":" not in cleaned:
        raise ValueError(f"Line {line_number}: Missing ':' separator")

    # Split only on the first colon to allow colons in ARNs
    name_part, arn_part = cleaned.split(":", 1)
    function_name = name_part.strip()
    function_arn = arn_part.strip()

    if not function_name:
        raise ValueError(f"Line {line_number}: Empty function name")
    if not function_arn.startswith("arn:aws:lambda:"):
        raise ValueError(f"Line {line_number}: Invalid Lambda ARN '{function_arn}'")

    return function_name, function_arn


def read_mapping_file(path: str) -> List[Tuple[str, str]]:
    pairs: List[Tuple[str, str]] = []
    with open(path, "r", encoding="utf-8") as f:
        for idx, raw in enumerate(f, start=1):
            try:
                parsed = parse_line(raw, idx)
            except ValueError as e:
                raise ValueError(str(e))
            if parsed:
                pairs.append(parsed)
    if not pairs:
        raise ValueError("Input file contained no valid mappings.")
    return pairs


def create_lambda_client(region: Optional[str], profile: Optional[str]):
    # Optionally select AWS profile (credentials) and region
    if profile:
        boto3.setup_default_session(profile_name=profile)
    client = boto3.client(
        "lambda",
        region_name=region,
        config=Config(retries={"max_attempts": 10, "mode": "standard"}),
    )
    return client


def update_memory_size(client, function_identifier: str, memory_size: int) -> None:
    # Use update_function_configuration with MemorySize
    client.update_function_configuration(
        FunctionName=function_identifier,  # ARN or name
        MemorySize=memory_size,
    )


def main():
    parser = argparse.ArgumentParser(
        description="Update AWS Lambda memory size for functions listed in a file."
    )
    parser.add_argument(
        "--file",
        required=True,
        help="Path to mapping file (lines like 'name: arn').",
    )
    parser.add_argument(
        "--memory",
        required=True,
        type=int,
        help="Desired memory size in MB (128–10240, in 1 MB increments).",
    )
    parser.add_argument(
        "--region",
        default=None,
        help="AWS region (e.g., us-east-1). If omitted, uses your default.",
    )
    parser.add_argument(
        "--profile",
        default=None,
        help="AWS profile name from your credentials.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned changes without applying.",
    )
    args = parser.parse_args()

    # Basic memory validation; AWS allows 128–10240, 1 MB increments
    if args.memory < 128 or args.memory > 10240:
        print("Memory must be between 128 and 10240 MB.", file=sys.stderr)
        sys.exit(2)

    try:
        pairs = read_mapping_file(args.file)
    except Exception as e:
        print(f"Failed to read mapping file: {e}", file=sys.stderr)
        sys.exit(2)

    print(f"Loaded {len(pairs)} function mappings from {args.file}")

    client = None
    if not args.dry_run:
        try:
            client = create_lambda_client(args.region, args.profile)
        except Exception as e:
            print(f"Failed to create Lambda client: {e}", file=sys.stderr)
            sys.exit(2)

    failures = 0
    for function_name, function_arn in pairs:
        identifier = function_arn  # Use ARN for precision
        if args.dry_run:
            print(f"[DRY-RUN] Would set {function_name} ({identifier}) memory to {args.memory} MB")
            continue

        try:
            update_memory_size(client, identifier, args.memory)
            print(f"Updated {function_name} ({identifier}) memory to {args.memory} MB")
        except (ClientError, BotoCoreError) as e:
            failures += 1
            print(f"FAILED to update {function_name} ({identifier}): {e}", file=sys.stderr)

    if failures:
        print(f"Completed with {failures} failures.", file=sys.stderr)
        sys.exit(1)
    else:
        print("All updates completed successfully.")


if __name__ == "__main__":
    main()


