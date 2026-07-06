"""Download and do all messages for microservice
@M-Malek
"""
from ztm_tools.sqs.receive_messages import receive_all_messages
from ztm_tools.sqs.error_message_handler import error_message_handler
from ztm_tools.logging.logger import main_logger

def accomplish_all_works(worker, task_handler):
    """
    Recive and accomplish all works
    :param worker:
    :param task_handler: dict; pairs of tasks for given worker [task_krypto: function]
    :return: None
    """
    sqs_messages = receive_all_messages(worker)
    for message in sqs_messages:
        # Accomplish job, take it from MongoDB collection events and send to status with status var: done
        # If error during job, add error information to payload, take message to errors
        task_name = message.payload["task"]
        handler = task_handler.get(task_name)
        if handler is None:
            error_message_handler(message)
            continue

        try:
            handler(message)
            main_logger("info", f"Task id {message.task_id} accomplished")
        except Exception as e:
            error_message_handler(message, e)


