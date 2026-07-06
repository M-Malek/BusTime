from ztm_tools.sqs.producer import message_producer
from ztm_tools.mongo_tools.mongo_connect import create_mongo_connection
from os import getenv
from src.s3_checking.s3_connect import s3_connect
from ztm_tools.logging.logger import main_logger

def create_message_statistic():
    """
    Create message statistic
    :return: None, create message statistic in SQS queue and MongoDB collection
    """
    payload = {
        "task": "statistic"
    }
    con = create_mongo_connection(getenv("MONGO_URI"))
    task_collection = con["Poznan"]["events"]
    sqs = s3_connect()
    message_producer(task_collection, sqs, "m4", "m3", payload)
    main_logger("info", "Created message statistic")
