from ztm_tools.mongo_tools.mongo_connect import create_mongo_connection
from ztm_tools.logging.logger import main_logger

def set_work_done_in_mongo(message, work_status):
    """
    Set work as done in MongoDB collection "Events" as done
    :param message: accomplished message
    :param work_status: work status
    :return:
    """
    con = create_mongo_connection()
    collection = con["Poznan"]["Events"]
    task_id = message["task_id"]
    result = collection.update_one({"task_id":task_id}, {"$set":{"status": work_status}})
    if result.matched_count == 0:
        main_logger("error", f"Cannot change status of task id: {message['task_id']} - task"
                             f"doesn't exist")

    con.close()
