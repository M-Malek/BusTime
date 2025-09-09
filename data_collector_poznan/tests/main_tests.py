"""
Main.py function tests
@M-Malek
"""
from data_collector_poznan.src.main import stops
from data_collector_poznan.src.db_sender.data_sender import connection_checker
import pymongo
from shared.tools.env_os_variables import db_uri
import data_collector_poznan.main


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


def test_two():
    """
    Testing how its work. Abort test after 20 minutes
    :return:
    """
    if __name__ == '__main__':
        data_collector_poznan.main


# test_one()
test_two()
