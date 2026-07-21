from ztm_tools.sqs.producer import message_producer
from ztm_tools.mongo_tools.mongo_connect import create_mongo_connection
from os import getenv
from src.s3_checking.s3_connect import s3_connect
from ztm_tools.logging.logger import main_logger
from src.mongo_micro_tools.get_active_url import get_active_url

def create_message_schedules():
    """
    Create message schedules
    :return: None, create message schedules in SQS queue and MongoDB collection
    """
    actual_url = get_active_url()
    payload = {
        "task": "schedules",
        "url": actual_url
    }
    con = create_mongo_connection(getenv("MONGO_URI"))
    task_collection = con["Poznan"]["Events"]
    sqs = s3_connect("S3_EVENTS_QUEUE")
    message_producer(task_collection,  "m4", "m3", payload, "Events")
    main_logger("info", "Created message schedules")

