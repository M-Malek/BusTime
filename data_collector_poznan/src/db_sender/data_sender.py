"""
Connect to MOngoDB database and save data:
- most actual timetables to Poznan/ZTM
- vehicles data once a 30 sec. to Poznan/Vehicles
"""
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


def connection(uri, type=1):
    """
    Establish connection with server and save data
    :param uri: connection string
    :param type: type of sender connection: 0 - save all, 1 - save vehicles, 2 - save schedules, default: 1
    :return: Data saved to db if connection was successfully; Exception e if connection failed
    """
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        print("Connection successfully achieved!")
        if type == 0:
            save_vehicles(client)
            save_timetables(client)
        elif type == 1:
            save_vehicles(client)
        elif type == 2:
            save_timetables(client)
        client.close()
    except Exception as e:
        print("An error during a connection: " + e)


def save_vehicles(clinet):
    """
    Każda z opcji danych musi mieć własny, osobny save! nie jedna funkcja od całości
    Po zrobieniu klasy posprzątaj program ze zbędnych danych!
    :param clinet:
    :return:
    """
    db_set = clinet["Poznan"]
    collection = db_set["Vehicles"]
    collection.insert_many()


def save_timetables(client):
    pass
