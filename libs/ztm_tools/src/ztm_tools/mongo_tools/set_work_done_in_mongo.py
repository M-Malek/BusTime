from ztm_tools.mongo_tools.mongo_connect import create_mongo_connection
from ztm_tools.logging.logger import main_logger
from json import loads
from os import getenv

def set_work_done_in_mongo(task_id, work_status, error=None):
    """
    Set work as done in MongoDB collection "Events" as done
    :param task_id: accomplished message
    :param work_status: work status
    :param error: error message
    :return: None
    """
    con = create_mongo_connection(getenv("MONGO_URI"))
    collection = con["Poznan"]["Events"]
    if error is not None:
        result = collection.update_one({"task_id":task_id}, {"$set":{"status": work_status, 'error': error}})
    else:
        result = collection.update_one({"task_id": task_id}, {"$set": {"status": work_status}})
    print(f'Debug: result: {result}')
    if result.matched_count == 0:
        main_logger("error", f"Cannot change status of task id: {'task_id'} - task"
                             f"doesn't exist")

    con.close()
