"""SQS Message Designer for ZTM Tools"""
from datetime import datetime
from ztm_tools.logging.logger import main_logger

# GLOBAL
MESSAGE_SET = {
    "task_id": "",
    "source": "",
    "worker": "",
    "date": None,
    "status": None,
    "payload": {}
}


def message_taks_id_creator(collection, source):
    """
    Create ID for message
    :param collection: MongoDB collection 'Events'
    :param source: source microservice
    :return: str, ID of message
    """
    print(f"Debug: given collection: {collection.name}")
    if not collection.name == "Events":
        main_logger("error", "Wrong collection name! Returning default task_id")
        today = str(datetime.now().strftime("%Y%m%d"))[2:]
        return today + source + "j" + "default"
    all_source_tasks = collection.find({"source": source})
    all_todays_tasks = []
    for entry in all_source_tasks:
        today = str(datetime.now().strftime("%Y%m%d"))[2:]
        date_from_db = entry["date"]
        date_from_db = str(date_from_db.strftime("%Y%m%d"))
        if today in date_from_db:
            all_todays_tasks.append(str(entry["task_id"]).split("j")[1])
    all_todays_tasks.sort(reverse=True)
    print(all_todays_tasks)
    if len(all_todays_tasks) == 0:
        # There is no entry for this day for this source - return id as first entry
        new_id = str(datetime.now().strftime("%Y%m%d"))[2:] + source + "j" + "0001"
    else:
        last_number = f"{(int(all_todays_tasks[0]) + 1):04d}"
        new_id = str(datetime.now().strftime("%Y%m%d"))[2:] + source + "j" + last_number
        print(new_id)
    return new_id

def message_creator(collection, source, worker, payload):
    """
    Create messsage for SQS
    :param collection: MongoDB collection 'Events' - archive of all messages
    :param source: source microservice - microservice which gives task
    :param worker: worker microservice - microservice which has to accomplish the task
    :param payload: dict, custom message payload
    :return: None, creates message and insert it into MongoDb, then into SQS
    """
    message_set = {
    "task_id": message_taks_id_creator(collection, source),
    "source": source,
    "worker": worker,
    "date": datetime.now(),
    "status": "pending",
    "payload": payload
    }
    return message_set
    # MESSAGE_SET["task_id"] = message_taks_id_creator(collection, source)
    # MESSAGE_SET["source"] = source
    # MESSAGE_SET["worker"] = worker
    # MESSAGE_SET["date"] = datetime.now()
    # MESSAGE_SET["status"] = "pending"
    # MESSAGE_SET["payload"] = payload
    # return MESSAGE_SET
