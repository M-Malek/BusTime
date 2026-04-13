import boto3
import json
import os
from datetime import datetime
import uuid
from src.log_logging import main_logger


sqs = boto3.client(
    "sqs",
    region_name="eu-central-1",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


QUEUE_URL = os.getenv("QUEUE_URL")
MESSAGES_SET = {
    # "vehicle_update": ("GTFS_UPDATED", ["feeds.pb", "vehicles.pb"]),
    # "vehicle_wipeout": ("GTFS_WIPEOUT", ["MONGO_DB"]),
    "stoptimes_normal": ("STOP_TIMES_NORMAL", "Microservice 2", "Create new vehicle data in S3"),
    "stoptimes_shapes": ("STOP_TIMES_SHAPES", "Microservice 2", "Download shapes data"),
    "stoptimes_stops": ("STOP_TIMES_STOPS", "Microservice 2", "Recreate stops information in MongoDB"),
    "statistic_normal": ("STATISTIC_NORMAL", "Microservice 3", "Generate new statistic from data")
}


def message_creator(event_type: str, worker: str, changed_files: list):
    """
    Generate automate message for Amazon SQS
    :param event_type: str: type of work to do from MESSAGES_SET global
    :param worker: str: worker type - information about Microservice, which has to complete this job
    :param changed_files: str: information about changes data in MongoDB or S3 from MESSAGES_SET
    :return: Ready SQS Message for AWS
    """
    message = {
            "event_id": str(uuid.uuid4()),
            "event_type": event_type,
            "source": "micro4_watcher",
            "timestamp": datetime.now().isoformat(),
            "payload": {
                        "worker": worker,
                        "changed_data": changed_files
                        }
            }
    return message


def send_event(message):

    message_body = message_creator()

    response = sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(message_body),
    )
    main_logger("info", f"New SQS message for {message} created. ID: {response['event_id']}")
