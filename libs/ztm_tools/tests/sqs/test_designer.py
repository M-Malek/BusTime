from ztm_tools.sqs.designer import message_taks_id_creator, message_creator
from ztm_tools.mongo_tools.mongo_connect import create_mongo_connection
from ztm_tools.mongo_tools.job_message_inserter import job_message_inserter
import datetime
from unittest.mock import patch

uri = "" # insert to accomplish tests
con = create_mongo_connection(uri)
col = con["Poznan"]


def test_message_taks_id_creator():
    task_id1 = message_taks_id_creator(col["Status"], "m4")
    assert task_id1 == "260702m4jdefault"

    task_id2 = message_taks_id_creator(col["Events"], "m4")
    assert task_id2 == "260702m4j0001"


def test_message_task_id_creator_with_message():
    message1 = {
        "task_id": "260702m4j0001",
        "source": "m4",
        "worker": "m2",
        "date": datetime.datetime.now(),
        "payload": {"test": None}
    }
    new_insert = job_message_inserter(col["Events"], message1)
    task_id3 = message_taks_id_creator(col["Events"], "m4")
    assert task_id3 == "260702m4j0002"

    message2 = {
        "task_id": "260702m4j0002",
        "source": "m4",
        "worker": "m2",
        "date": datetime.datetime.now(),
        "payload": {"test": None}
    }
    new_insert = job_message_inserter(col["Events"], message2)
    task_id4 = message_taks_id_creator(col["Events"], "m4")
    assert task_id4 == "260702m4j0003"

    # All tests for message_id_creator passed


@patch("ztm_tools.sqs.designer.datetime")
def test_message_creator(mock_datetime):
    fixed_time = datetime.datetime(2026, 7, 2, 12, 0, 0)
    mock_datetime.now.return_value = fixed_time
    message = message_creator(col["Events"], "m4", "m3", {"test": "ok"})
    result_message = {
    "task_id": "",
    "source": "m4",
    "worker": "m3",
    "date": fixed_time,
    "status": "pending",
    "payload": {
        "test": "ok"
    }
    }
    assert message["source"] == result_message["source"], (f"Wrong source: {message['source']} "
                                                           f"instead of {result_message['source']} ")
    assert message["worker"] == result_message["worker"], (f"Wrong worker: {message['worker']} "
                                                           f"instead of {result_message['worker']} ")
    assert message["status"] == result_message["status"], (f"Wrong status: {message['status']} "
                                                           f"instead of {result_message['status']} ")
    assert message["payload"] == result_message["payload"], (f"Wrong payload: {message['payload']} "
                                                           f"instead of {result_message['payload']} ")
    # Test passed
