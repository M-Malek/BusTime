"""ZTM messages consumer for ZTM Tools"""
import boto3
import os
import json


def receive_all_messages(worker: str):
    """Recive all messages from SQS queue for a given worker
    Args:
        worker (str): Worker name to filter messages by
        Returns:
            list: List of messages for the given worker
            """
    
    messages = []
    sqs = boto3.client(
        "sqs",
        endpoint_url=os.getenv("S3_ENDPOINT"),
        region_name="elasticmq",
        aws_access_key_id="x",
        aws_secret_access_key="x"
    )

    while True:
        queue_url = sqs.get_queue_url(QueueName="events")["QueueUrl"]
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=1
        )

        batch = response.get("Messages", [])
        
        for message in batch:
            body = json.loads(message["Body"])
            if body["worker"] == worker:
                messages.append(worker)

        if not batch:
            break

        messages.extend(batch)

    return messages


def delete_message(msg: dict, queue_name: str):
    """Deletes a mmessage from the SQS queue"""
    
    queue_url = os.getenv("SQS_QUEUE_URL")
    sqs = boto3.client(
        "sqs",
        endpoint_url=os.getenv("S3_ENDPOINT"),
        region_name="elasticmq",
        aws_access_key_id="x",
        aws_secret_access_key="x"
    )
    queue_url = sqs.get_queue_url(QueueName=queue_name)["QueueUrl"]
    sqs.delete_message(
        QueueUrl = queue_url,
        ReceiptHandle = msg["ReceiptHandle"]
    )
    