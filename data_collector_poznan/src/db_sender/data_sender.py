"""
Connect to MOngoDB database and save data:
- most actual timetables to Poznan/ZTM
- vehicles data once a 30 sec. to Poznan/Vehicles
"""
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


def connection(uri):
    """
    Establish connection with server and save data
    :param uri: connection string
    :return: Data saved to db if connection was successfully; Exception e if connection failed
    """
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        print("Connection successfully achieved!")
        save_vehicles()
        save_timetables()
        client.close()
    except Exception as e:
        print("An error during a connection: " + e)


def save_vehicles():
    pass


def save_timetables():
    pass
