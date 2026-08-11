from src.logic.stoptime_watcher_logic import organize_documents_state
from ztm_tools.mongo_tools.mongo_connect import create_mongo_connection
from os import getenv

def test_one_organize_document_state():
    """
    Tests on live database
    :return:
    """
    # Test one: there is no entry with state: 'active', actual_entry_id == None
    organize_documents_state()

    # Check
    connection = create_mongo_connection(getenv("MONGO_URI"))
    print(connection["Poznan"].list_collection_names())
    print(getenv("MONGO_URI"))
    coll = connection["Poznan"]["Stop_times_arch"]
    assert coll.count_documents({'state': 'active'}) == 1, 'Test with actual_entry_id is None failed'
    # Test passed

def test_two_organize_document_state():
    # Test two: there is no entry with state: 'active', actual_entry_id == random id
    # Random_id - that's mean that I have chosen one entry, set its state as 'active' and take its _id
    organize_documents_state('6a7b595436242a9819c5bb09')

    # Check
    connection = create_mongo_connection(getenv("MONGO_URI"))
    coll = connection["Poznan"]["Stop_times_arch"]
    assert coll.count_documents({'state': 'active'}) == 1, 'Test with actual_entry_id has random id failed'
    # Test passed
