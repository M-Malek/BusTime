"""
Read all messages from SQS queue for given worker
:author: @M-Malek
"""
from json import loads

def sqs_message_reader(sqs, queue, worker):
    """
    Read message from SQS queue for given worker
    :param sqs: sqs connection
    :param queue: str, name of the queue to read messages
    :param worker: str, name of the worker
    :return: list with all messages
    """
    while True:
        queue_url = sqs.get_queue_url(QueueName=queue)["QueueUrl"]
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=5
        )
        # 2. Check if there is any message
        batch = response.get("Messages", [])

        # If there is no message - break
        if not batch:
            break

        # 3. Check if message is for given worker and return it
        message = batch[0]
        body = loads(message["Body"])

        if body["worker"] == worker:
            return message
