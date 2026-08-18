"""
Main function to connect to SQS Messages queue
:author: @M-Malek
"""
import boto3
from os import getenv
from ztm_tools.logging.logger import main_logger

def sqs_connector():
    """
    Function to collect SQS messages from SQS Messages queue for given worker
    :param queue: str, name of queue
    :return: dict, all messages from SQS queue for given worker
    """

    messages = []
    attempts = 3
    # 1. Establish connection with SQS with 3 attempts
    for i in range(0, 4):
        try:
            sqs = boto3.client(
                "sqs",
                endpoint_url=getenv("S3_ENDPOINT"),
                region_name="elasticmq",
                aws_access_key_id="x",
                aws_secret_access_key="x"
            )
        except Exception as e:
            main_logger("error", f"Error connecting to SQS: {e}")
            attempts -= 1

    if attempts == 0:
        main_logger("error", f"Connection to SQS failed.")
        return Exception
    else:
        return sqs
