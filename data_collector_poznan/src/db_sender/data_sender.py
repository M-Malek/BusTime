"""
Connect to MongoDB database and save data:
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
    :return: Information if connection was successfully or Exception e if connection failed
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
    :param data: pandas.DataFrame: prepared Vehicle data
    :return: nothing, saving data in db
    """
    client = MongoClient(uri, server_api=ServerApi('1'))
    db_set = client["Poznan"]
    collection = db_set["Vehicles"]
    collection.insert_many(data.to_dict("records"))
    client.close()


def save_timetables(uri, data_lvi, data_sh, data_st):
    """
    Save data from .zip file to database
    :param uri: MongoDB Client URI
    :param data_lvi: pandas.DataFrame: prepared line route info data
    :param data_sh: pandas.DataFrame: prepared shape data
    :param data_st: pandas.DataFrame: prepared stops times data
    :return: nothing, saving data in db
    """
    client = MongoClient(uri, server_api=ServerApi('1'))
    db_set = client["Poznan"]
    collection_lvi = db_set["Line_info"]
    collection_lvi.insert_many(data_lvi.to_dict("records"))
    collection_sh = db_set["Shapes"]
    collection_sh.insert_many(data_sh.to_dict("records"))
    collection_st = db_set["Stop_times"]
    collection_st.insert_many(data_st.to_dict("records"))
    client.close()


def save_stops(uri, stops):
    """
    Save actual stops data to database
    :param uri: MongoDB Client URI
    :param stops: pandas.DataFrame: stops data
    :return: nothing
    """
    client = MongoClient(uri, server_api=ServerApi('1'))
    db_set = client["Poznan"]
    collection_st = db_set["Stops"]
    collection_st.insert_many(stops.to_dict("records"))
    # for index, row in stops.iterrows():
    #     collection_st.insert_one(row)
    client.close()
