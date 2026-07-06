"""SQS messages producer for ZTM Tools"""
from ztm_tools.mongo_tools import job_message_inserter
from ztm_tools.sqs.designer import message_creator
from ztm_tools.mongo_tools.job_message_inserter import job_message_inserter
from ztm_tools.sqs.sender import send_message
from ztm_tools.logging.logger import main_logger

def message_producer(collection, sqs, source, worker, payload):
    """
    Send message to SQS with creation of history of message in MongoDB
    :param collection: MongoDB collection where we save messages history
    :param sqs: SQS queues
    :param source: Microservice which is source of message, e.g. m4
    :param worker: Microservice which is worker of message, e.g. m3
    :param payload: message payload for microservice
    :return: None, saving message to SQS queue and mongodb collection
    """
    message = message_creator(collection, sqs, source, worker, payload)
    var_create_job_in_history = job_message_inserter()
    if not var_create_job_in_history:
        var_send_job = send_message(message)
        if type(var_send_job) is list:
            main_logger("error", "Sending message to SQS failed.")
        main_logger("info", f"Message sent to SQS. Message ID in MongoDB: {var_send_job}")
    else:
        main_logger("error", "Cannot save message in history. Sending message aboard")



