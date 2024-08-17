"""Configuration."""

from pathlib import Path
import yaml

with open("config.yaml", "r") as file:
    aws_config = yaml.safe_load(file)


def get_dataset_filepath() -> Path:
    return aws_config["dataset"]["filepath"]


def get_s3_bucket_name() -> str:
    """Get S3 bucket name to store the csv file."""
    bucket_name = aws_config["aws"]["s3_bucket_name"]
    if not bucket_name:
        raise KeyError(f"No value set for aws s3_bucket_name in config.yaml")
    return bucket_name


def get_kinesis_stream_name() -> str:
    """Get Kinesis stream name."""
    stream_name = aws_config["aws"]["kinesis_stream_name"]
    if not stream_name:
        raise KeyError(f"No value set for aws kinesis_stream_name in config.yaml")
    return stream_name


def get_ecr_repo_name() -> str:
    ecr_repo_name = aws_config["aws"]["ecr_repo_name"]
    if not ecr_repo_name:
        raise KeyError(f"No value set for aws ecr_repo_name in config.yaml")
    return ecr_repo_name


def get_notifications_email() -> str:
    return aws_config["aws"]["notifications_email"]


def billing_alarm_threshold() -> int:
    """Get CloudWatch billing alarm threshold."""
    return aws_config["aws"]["cloudwatch_billing_alarm_threshold_eur"]
