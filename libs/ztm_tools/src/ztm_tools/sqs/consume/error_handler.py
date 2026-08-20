"""
Handle errors related to task execution
:author: @M-Malek
"""
from ztm_tools.logging.logger import main_logger
from json import dumps, loads
from ztm_tools.mongo_tools.set_work_done_in_mongo import set_work_done_in_mongo

def error_handler(sqs, message, error = None):
    """
    Handle a message which failed after all retry attempts.
    The failed message is sent to the status queue and removed from the events queue.
    :param sqs: SQS connection
    :param message: message with all parameters
    :param error: optional error information
    :return: Nothing
    """

    # Read message id
    task_id = loads(message['Body'])["task_id"]
    body = loads(message['Body'])
    # Prepare message information
    status_message = {
        "task_id": task_id,
        "source": body["source"],
        "worker": body["worker"],
        "status": "failed",
        "error": str(error) if error else None,
        "payload": body["payload"]
    }

    # Read status and events queue urls
    status_queue_url = sqs.get_queue_url(QueueName="status")["QueueUrl"]
    events_queue_url = sqs.get_queue_url(QueueName="events")["QueueUrl"]

    try:
        # Give information to MongoDB that given task is failed
        set_work_done_in_mongo(task_id, "failed", error if error else None)
        # 1. Send information about failed task to status queue
        sqs.send_message(
            QueueUrl=status_queue_url,
            MessageBody=dumps(status_message)
        )

        # 2. Remove original message from events queue
        sqs.delete_message(
            QueueUrl=events_queue_url,
            ReceiptHandle=message["ReceiptHandle"]
        )

        # 3. Log - message removed to status queue
        main_logger(
            "error",
            f"Task {task_id} failed after all attempts. "
            f"Moved to status queue."
        )

    except Exception as exc:
        # 4. Log - cannot move task!
        main_logger(
            "error",
            f"Error handler failed for task {task_id}: {exc}"
        )
    