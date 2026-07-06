from datetime import datetime

import bson

import pymongo
from ztm_tools.mongo_tools.job_message_inserter import job_message_inserter
from ztm_tools.mongo_tools.mongo_connect import create_mongo_connection
import os
from bson import ObjectId

def test_live_job_message_inserter():
    uri = "" # add URI before test starts
    # con = create_mongo_connection(os.getenv("MONGO_URI"))
    con = create_mongo_connection(uri)
    col = con["Poznan"]["Events"]
    print(col)
    message1 = {
        "task_id": "test_1",
        "source": "tester_sender",
        "worker": "tester_worker",
        "date": datetime.now(),
        "payload": {
            "task": "test_job",
            "url": "test_job_url"
        }
    }
    test_job1 = job_message_inserter(col, message1)
    print(test_job1)
    doc = col.find_one({"_id": test_job1})
    print(doc)
    assert col.find_one({"_id": test_job1}) is not None
    assert isinstance(test_job1, ObjectId) == True, "Error"

    message2 = {
        "task_id": "test_2",
        "source": "tester_sender",
        "worker": "tester_worker",
        "date": datetime.now(),
        "payload": {
            "task": "test_job_statistic",
            "url": "test_job_url",
            "yyymm": "cokolwiek"
        }
    }
    test_job2 = job_message_inserter(col, message2)
    print(test_job2)
    assert col.find_one({"_id": test_job1}) is not None
    assert isinstance(test_job2, ObjectId) == True, "Error"

    # All test passed