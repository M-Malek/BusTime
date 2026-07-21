"""SQS messages producer for ZTM Tools"""
from ztm_tools.mongo_tools import job_message_inserter
from ztm_tools.sqs.designer import message_creator
from ztm_tools.mongo_tools.job_message_inserter import job_message_inserter
from ztm_tools.sqs.sender import send_message
from ztm_tools.logging.logger import main_logger

def message_producer(collection, source, worker, payload, queue):
    """
    Send message to SQS with creation of history of message in MongoDB
    :param collection: MongoDB collection where we save messages history
    :param sqs: SQS queues
    :param source: Microservice which is source of message, e.g. m4
    :param worker: Microservice which is worker of message, e.g. m3
    :param payload: message payload for microservice
    :param queue: SQS queue name
    :return: None, saving message to SQS queue and mongodb collection
    """
    message = message_creator(collection, source, worker, payload)
    var_create_job_in_history = job_message_inserter(collection, message)
    print(f"Debug: {var_create_job_in_history}")
    if type(var_create_job_in_history) == list:
        # There were errors during saving job message in Events collection in MongoDB
        main_logger("error", "Cannot save message in history. Sending message aboard")
    else:
        # Saving job message in Events collection in MongoDB accomplished
        var_send_job = send_message(message, queue)
        print(f"Debug: {type(var_send_job)}")
        # var_send_job = send_message(message, queue)
        print(f"Debug: {type(var_send_job)}")
        if type(var_send_job) is list:
            # There were errors during saving job message to SQS
            main_logger("error", "Sending message to SQS failed.")
        else:
            main_logger("info", f"Message sent to SQS. Message ID in MongoDB: {var_send_job}")
