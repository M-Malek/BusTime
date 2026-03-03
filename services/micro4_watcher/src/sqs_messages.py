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
    "vehicle_update": ("GTFS_UPDATED", ["feeds.pb", "vehicles.pb"]),
    "vehicle_wipeout": ("GTFS_WIPEOUT", ["MONGO_DB"]),
    "stoptimes_normal": ("STOP_TIMES_NORMAL", ["stop_times.txt", "agency.txt", "routes.txt", "trips.txt"]),
    "stoptimes_shapes": ("STOP_TIMES_SHAPES", ["shapes.txt"]),
    "stoptimes_stops": ("STOP_TIMES_STOPS", ["stops.txt"]),
    "statistic_normal": ("STATISTIC_NORMAL", ["MONGO_DB"])
}


def message_creator(event_type: str, changed_files: list):
    """
    Generate automate message for Amazon SQS
    :param event_type:
    :param changed_files:
    :return: Ready SQS Message for AWS
    """
    message = {
            "event_id": str(uuid.uuid4()),
            "event_type": event_type,
            "source": "micro4_watcher",
            "timestamp": datetime.now().isoformat(),
            "payload": {
                        "stop_times_date": "2026-03-02",
                        "changed_files": changed_files
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
