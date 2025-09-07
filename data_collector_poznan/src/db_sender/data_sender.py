"""
Connect to MOngoDB database and save data:
- most actual timetables to Poznan/ZTM
- vehicles data once a 30 sec. to Poznan/Vehicles
"""
# For data sending
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

#  For data gater:
from data_collector_poznan.src.parser.feeds_collector import feeds_manager
from data_collector_poznan.src.parser.zip_collector import SchedulesCollector
from data_collector_poznan.src.gather.zip_gather import schedules_downloader

# env os variables:
from shared.tools.env_os_variables import feed_link, vehicle_link


def connection_checker(uri):
    """
    Check connection with database
    :param uri: connection string
    :param sending_type: type of sender connection: 0 - save all, 1 - save vehicles, 2 - save schedules, default: 1
    :return: Data saved to db if connection was successfully; Exception e if connection failed
    """
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        print("Connection successfully achieved!")
        client.close()
    except Exception as e:
        print("An error during a connection: " + e)


def save_vehicles(uri, data):
    """
    Save vehicles information to database
    :param uri: MongoDB Client URI
    :param data: prepared Vehicle data
    :return: saving data in db
    """
    client = MongoClient(uri, server_api=ServerApi('1'))
    db_set = client["Poznan"]
    collection = db_set["Vehicles"]
    collection.insert_many(data)
    client.close()


def save_timetables(uri, data):
    """
    Save data from .zip file to database
    :param uri: MongoDB Client URI
    :param data: prepared schedules data
    :return: saving data in db
    """
    client = MongoClient(uri, server_api=ServerApi('1'))
    # db_set = client["Poznan"]
    # collection = db_set["Vehicles"]
    # collection.insert_many(data)
    client.close()
