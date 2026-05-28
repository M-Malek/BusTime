"""ZTM messages consumer for ZTM Tools"""
from boto3 import client
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
    queue_url = os.getenv("SQS_QUEUE_URL")
    
    sqs = client("sqs")

    while True:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=1
        )

        batch = response.get("Messages", [])
        
        for message in batch:
            body = json.loads(message["Body"])
            if body["payload"]["worker"] == worker:
                messages.append(worker)

        if not batch:
            break

        messages.extend(batch)

    return messages


def delete_message(msg: dict):
    """Deletes a mmessage from the SQS queue"""
    
    queue_url = os.getenv("SQS_QUEUE_URL")
    sqs = client("sgs")
    sqs.delete_message(
        QueueUrl = queue_url,
        ReceiptHandle = msg["ReceiptHandle"]
    )
    