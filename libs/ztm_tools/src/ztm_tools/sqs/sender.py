"""Send message to SQS queue"""
import json
import os
import uuid
from datetime import datetime, timezone
from botocore.exceptions import ClientError, EndpointConnectionError

import boto3
from ztm_tools.logging.logger import main_logger

def send_message(message_set: dict, queue: str):
    """
    Send event to SQS
    :param message_set: dict, ready by func message_creator dictionary with SQS message
    :param queue: str, SQS queue name
    :return: error_logs: list of error messages
    """
    main_logger("info", f"Debug: Queue: '{queue}' ({type(queue)})")
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
            # response = sqs.list_queues()
            # print(f"Debug: list_queues response: {response}")
            if queue == "Events":
                queue_url = sqs.get_queue_url(QueueName="events")["QueueUrl"]
                response = sqs.send_message(
                    QueueUrl=queue_url,
                    MessageBody=json.dumps(message_body, default=str),
                )
                print("Debug from send_message: Events: ", response["MessageId"])
            elif queue == "Status":
                queue_url = sqs.get_queue_url(QueueName="status")["QueueUrl"]
                response = sqs.send_message(
                    QueueUrl=queue_url,
                    MessageBody=json.dumps(message_body, default=str),
                )
                print("Debug from send_message: Status: ", response["MessageId"])
            else:
                raise ValueError("No valid queue name provided")
            # print(type(message_set))
            main_logger("info", f"New SQS message for {message_set} created. ID: "
                                f"{response['MessageId']}")
            break
        except Exception as e:
            if e == "EndpointConnectionError":
                main_logger("warning", f"Sending SQS message for {message_set['task_id']} failed. "
                                   f"No connection with SQS. "
                                   f"Attempts left: {sqs_attempts}")
                error_logs.append(e)
            elif e == "ClientError":
                code = e.response['Error']['Code']

                if code == 'AccessDenied':
                    main_logger("warning", f"Sending SQS message for {message_set['task_id']} failed."
                                       f"Access denied. "
                                       f"Attempts left: {sqs_attempts}")
                    error_logs.append(e)
                elif code == 'AWS.SimpleQueueService.NonExistentQueue':
                    main_logger("warning", f"Sending SQS message for {message_set['task_id']}failed. "
                                       f"No SQS queue. "
                                       f"Attempts left: {sqs_attempts}")
                    error_logs.append(e)
            else:
                main_logger("warning", f"Sending SQS message for {message_set['task_id']} failed. "
                                   f"Unknown error: {e}. "
                                   f"Attempts left: {sqs_attempts}")
                error_logs.append(e)
                main_logger("warning", f"{type(e).__name__}: {e!r}")

        sqs_attempts -= 1

    if sqs_attempts == 0:
        main_logger("error", f"SQS message for {message_set[1]} cannot be saved in SQS!")
    return  error_logs

"""
NIe działa numerowanie jak nie wysyłają się prawidłowo wiadomości do archiwum - jak się nie wyślą to i tak nie zadziała!
NIe działa wykrywanie plików .ztm - aktualny wykrywa prawidłowo ale nadchodzący dostaje status 'archive' zamiast 
'pending' - działa to wybiórczo
"""