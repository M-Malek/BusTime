def check_message_accomplished(task_id, con):
    """
    Check, if given task_id is accomplished or not
    :param task_id: task id
    :param con: MongoDB collection with tasks to examine
    :return: True if task_id is accomplished else False
    """
    for entry in con:
        if entry.task_id == task_id:
            if entry.status == "Accomplished":
                return True
    return False