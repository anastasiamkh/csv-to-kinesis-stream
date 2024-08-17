import boto3
import csv

import logging

import src.config as config
from src.utils_s3 import download_file_from_s3

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


s3_client = boto3.client("s3")
kinesis_client = boto3.client("kinesis")


class CSVtoStream:
    def __init__(self):
        """Read the environmental variables."""
        self.bucket_name: str = config.get_s3_bucket_name()
        self.dataset_filepath: str = config.get_dataset_filepath()
        self.kinesis_stream_name: str = config.get_kinesis_stream_name()

        # clients to connect to AWS services
        self._kinesis_client = boto3.client("kinesis")
        self._s3_client = s3_client

    def load_dataset(self):
        response = download_file_from_s3(
            bucket_name=self.bucket_name, filepath=self.dataset_filepath
        )

        # parse the file
        file_content = response["Body"].read().decode("utf-8").splitlines()

        return file_content

    def start_stream(self) -> None:
        """Conevrt rows in csv file on AWS S3 to events in AWS Kinesis stream"""

        csv_reader = csv.reader(self.load_dataset())

        logger.info(
            {
                "message": "Starting Kinesis stream",
                "dataset_filepath": self.dataset_filepath,
                "s3_bucket": self.bucket_name,
                "kinesis_stream_name": self.kinesis_stream_name,
            }
        )
        # Process each row in the CSV file and send it to the Kinesis stream
        for row in csv_reader:
            data = ",".join(row)
            logging.info(f"Streaming row to Kinesis: {data}")
            kinesis_client.put_record(
                StreamName=self.kinesis_stream_name,
                Data=data,
                PartitionKey=row[
                    0
                ],  # Assuming the first column can be used as a partition key
            )

        logger.info(
            {
                "message": "Streaming to Kinesis complete. No more rows to stream",
                "dataset_filepath": self.dataset_filepath,
                "s3_bucket": self.bucket_name,
                "kinesis_stream_name": self.kinesis_stream_name,
            }
        )

        return {"statusCode": 200, "body": "Finished streaming data."}


if __name__ == "__main__":
    CSVtoStream().start_stream()
