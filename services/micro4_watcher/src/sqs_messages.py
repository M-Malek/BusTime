import json
import os
import uuid
from datetime import datetime, timezone
from botocore.exceptions import ClientError, EndpointConnectionError

import boto3
from trash.log_logging import main_logger

QUEUE_URL = os.getenv("QUEUE_URL")


def message_creator(message_set: tuple):
    """
    Generate automate message for Amazon SQS
    "param message_set: tuple from MESSAGE_SET global with parameters:
        event_type = message_set[0]
        worker = message_set[1]
        change_type = message_set[2]
        job = message_set[3]
        location = message_set[4]
    :return: message: dict - Ready SQS Message for AWS
    """
    # print(f"Debug in message_creator: {message_set}")
    # print(type(message_set))
    event_type = message_set[0]
    worker = message_set[1]
    change_type = message_set[2]
    job = message_set[3]
    location = message_set[4]
    message = {
            "event_id": str(uuid.uuid4()),
            "event_type": event_type,
            "source": "micro4_watcher",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": {
                        "worker": worker,
                        "changed_data": {
                            "type": change_type,
                            "action": job,
                            "location": location
                            }
                        }
            }
    return message


def send_event(message_set: dict):
    """
    Send event to SQS
    :param message_set: dict, ready by func message_creator dictionary with SQS message
    :return:
    """

    # message_body = message_creator(message_set)
    message_body = message_set
    sqs_attempts = 3
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
        except EndpointConnectionError:
            main_logger("warning", f"Sending SQS message for {message_set[1]} failed. "
                                   f"No connection with SQS. "
                                   f"Attempts left: {sqs_attempts}")
        except ClientError as e:
            code = e.response['Error']['Code']

            if code == 'AccessDenied':
                main_logger("warning", f"Sending SQS message for {message_set[1]} failed."
                                       f"Access denied. "
                                       f"Attempts left: {sqs_attempts}")
            elif code == 'AWS.SimpleQueueService.NonExistentQueue':
                main_logger("warning", f"Sending SQS message for {message_set[1]} failed. "
                                       f"No SQS queue. "
                                       f"Attempts left: {sqs_attempts}")
        except Exception as e:
            main_logger("warning", f"Sending SQS message for {message_set[1]} failed. "
                                   f"Unknown error: {e}. "
                                   f"Attempts left: {sqs_attempts}")

        sqs_attempts -= 1

    if sqs_attempts == 0:
        main_logger("error", f"SQS message for {message_set[1]} cannot be saved in SQS!")

