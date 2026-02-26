import boto3
import json
import os
from src.micro_jobs import job_stops, job_shapes, job_normal

sqs = boto3.client(
    "sqs",
    region_name="eu-central-1",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

QUEUE_URL = os.getenv("QUEUE_URL")

EVENT_HANDLERS = {
    "STOP_TIMES_NORMAL": job_normal,
    "STOP_TIMES_SHAPES": job_shapes,
    "STOP_TIMES_STOPS": job_stops,
}


def process_message(body: dict):
    event_type = body["type"]
    payload = body.get("payload", {})

    handler = EVENT_HANDLERS.get(event_type)

    if not handler:
        raise ValueError(f"Unknown event type: {event_type}")

    handler(payload)


def consume():
    response = sqs.receive_message(
        QueueUrl=QUEUE_URL,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10  # long polling
    )

    messages = response.get("Messages", [])

    for message in messages:
        body = json.loads(message["MessageBody"])

        try:
            process_message(body)

            # Job is done
            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=message["ReceiptHandle"]
            )

            print("Message deleted (job done).")

        except Exception as e:
            print("Error:", e)
            # jobs went back to queue

#
# if __name__ == "__main__":
#     consume()
