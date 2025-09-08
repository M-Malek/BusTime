"""
Main.py function tests
@M-Malek
"""
from data_collector_poznan.src.main import stops
from data_collector_poznan.src.db_sender.data_sender import connection_checker
import pymongo
from shared.tools.env_os_variables import db_uri


def test_one():
    """
    Checking posibility to save data in Database
    :return:
    """
    connection_checker(db_uri)
    stops()
    client = pymongo.MongoClient(db_uri)
    db = client["Poznan"]
    db_set = db["Stops"]
    result = db_set.find_one()
    print(result)


test_one()
