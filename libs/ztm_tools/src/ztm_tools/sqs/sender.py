"""Send message to SQS queue"""
import json
import os
import uuid
from datetime import datetime, timezone
from botocore.exceptions import ClientError, EndpointConnectionError

import boto3
from trash.log_logging import main_logger

def send_message(message_set: dict):
    """
    Send event to SQS
    :param message_set: dict, ready by func message_creator dictionary with SQS message
    :return: error_logs: list of error messages
    """

    # message_body = message_creator(message_set)
    message_body = message_set
    sqs_attempts = 5
    error_logs = []
    # print("Debug: starting to send message to SQS")
    while sqs_attempts >= 0:
        try:
            """
            <--- Amazon SQS code section --->
            Turned off for offline testing with ElastiqMQ. In production, replace ElasticMQ code section with this code
            below:
            sqs = boto3.client(
                "sqs",
                region_name="eu-central-1",
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            )
            """
            """<--- ElasticMQ code section --->"""
            sqs = boto3.client(
                "sqs",
                endpoint_url=os.getenv("S3_ENDPOINT"),
                region_name="elasticmq",
                aws_access_key_id="x",
                aws_secret_access_key="x"
            )
            # print("Debug: połączono z SQS")
            response = sqs.send_message(
                QueueUrl=os.getenv("S3_QUEUE_URL"),
                MessageBody=json.dumps(message_body),
            )
            # print(type(message_set))
            main_logger("info", f"New SQS message for {message_set} created. ID: "
                                f"{response['MessageId']}")
            break
        except EndpointConnectionError as no_con:
            main_logger("warning", f"Sending SQS message for {message_set[1]} failed. "
                                   f"No connection with SQS. "
                                   f"Attempts left: {sqs_attempts}")
            error_logs.append(no_con)
        except ClientError as e:
            code = e.response['Error']['Code']

            if code == 'AccessDenied':
                main_logger("warning", f"Sending SQS message for {message_set[1]} failed."
                                       f"Access denied. "
                                       f"Attempts left: {sqs_attempts}")
                error_logs.append(e)
            elif code == 'AWS.SimpleQueueService.NonExistentQueue':
                main_logger("warning", f"Sending SQS message for {message_set[1]} failed. "
                                       f"No SQS queue. "
                                       f"Attempts left: {sqs_attempts}")
                error_logs.append(e)
        except Exception as e:
            main_logger("warning", f"Sending SQS message for {message_set[1]} failed. "
                                   f"Unknown error: {e}. "
                                   f"Attempts left: {sqs_attempts}")
            error_logs.append(e)

        sqs_attempts -= 1

    if sqs_attempts == 0:
        main_logger("error", f"SQS message for {message_set[1]} cannot be saved in SQS!")
    return  error_logs