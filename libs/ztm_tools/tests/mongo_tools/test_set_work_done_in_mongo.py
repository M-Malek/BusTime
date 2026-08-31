from ztm_tools.mongo_tools.set_work_done_in_mongo import set_work_done_in_mongo
from ztm_tools.mongo_tools.mongo_connect import create_mongo_connection
from os import environ


# Load S3_ENDPOINT to .env variables from hand
# delete after test / add to test!
environ["MONGO_URI"] = ""
MONGO_URI = environ["MONGO_URI"]

def test_set_work_done_in_mongo():
    """Test set_work_done_in_mongo, test with live database!"""
    task_id = '260723m4j0005'
    error = "text for test error"
    work_status = 'test error'

    set_work_done_in_mongo(task_id, work_status, error)

    # Check if message has been correctly updated
    con = create_mongo_connection(MONGO_URI)
    collection = con["Poznan"]["Events"]
    result = collection.find_one({"task_id":task_id})
    assert result['error'] == error, 'Error with modifying entry!'
