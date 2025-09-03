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


def connection(uri, sending_type=1):
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
        if sending_type == 0:
            save_vehicles(client, vehicle_link, feed_link)
            save_timetables(client)
        elif sending_type == 1:
            save_vehicles(client, vehicle_link, feed_link)
        elif sending_type == 2:
            save_timetables(client)
        client.close()
    except Exception as e:
        print("An error during a connection: " + e)


def save_vehicles(client, v_link, f_link):
    """
    Każda z opcji danych musi mieć własny, osobny save! nie jedna funkcja od całości
    Po zrobieniu klasy posprzątaj program ze zbędnych danych!
    :param v_link: vehicle.pb url
    :param f_link: feeds.pb url
    :param client: MongoDB Client URI
    :return: saving data in db
    """
    vehicle = feeds_manager(v_link, f_link)
    db_set = client["Poznan"]
    collection = db_set["Vehicles"]
    collection.insert_many(vehicle)


def save_timetables(client, zip_link):
    """
    Save data from .zip file to database
    :param client: MongoDB Client URI
    :param zip_link: ZTM .zip
    :return:
    """
    pass
