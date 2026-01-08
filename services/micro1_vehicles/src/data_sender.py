"""
Data_sender file - check and establish connection with MongoDB, then save data to Vehicle table
@M-Malek
"""

# Libs
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from shared.tools.log_logging import main_logger
from shared.tools.env_os_variables import db_uri


# Small companion function to db management and connection check
def connection_establisher(uri):
    """
    Check and establish connection with given MongoDB database
    :param uri: MongoDB uri
    :return: connected MongoDB client
    """
    try:
        client = MongoClient(uri, server_api=ServerApi('1'))
        client.admin.command('ping')
        return client
    except Exception as e:
        main_logger("error", f"Error during connection with MongoDB: {e}")
        return False


def connection_checker(uri):
    """
    Check connection with database
    :param uri: connection string
    :return: Information if connection was successfully or Exception e if connection failed
    """
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        # print("Connection successfully achieved!")
        main_logger("info", "Test connection with MongoDB - success!")
        client.close()
        return True
    except Exception as e:
        print("An error during a connection: " + e)
        main_logger("error", f"Error during connection with MongoDB: {e}")
        return False


def db_data_wipeout(uri, tables):
    if not connection_checker(uri):
        # print("Database currently unavailable. Data wipeout failed")
        main_logger("error", "Database currently unavailable. Data wipeout failed")
        return None

    # print(f"Starting data wipeout from collections: {tables}")
    main_logger("warning", f"Starting data wipeout from collections: {tables}")
    client = MongoClient(uri, server_api=ServerApi('1'))
    db_set = client["Poznan"]
    for table in tables:
        # Debug:
        # print(f"{table} type: {type(table)}")
        collection = db_set[table]
        collection.drop()
    client.close()
    # print(f"Data wipe outed!")
    main_logger("warning", "Data wipe outed!")


def data_check(uri, tables):
    """
    Function to download small peace of data to check its quality
    :param uri: MongoDB connection uri
    :param tables: table name or tables names for which check data
    :return: list with data: each list element contains list of 5 data probe from tables described by tables
    """
    if not connection_checker(uri):
        # print("Database currently unavailable. Data wipeout failed")
        main_logger("error", "Database currently unavailable. Data check failed")
        return None

    result_list = []
    client = MongoClient(uri, server_api=ServerApi('1'))
    db_set = client["Poznan"]
    for table in tables:
        collection = db_set[table]
        random_docs = list(collection.aggregate([
            {"$sample": {"size": 5}}
        ]))
        result_list.append(random_docs)
    return result_list


# Main saving functions:
# WARNING: replace uri on client to save resources with savings file basic operations!
def save_vehicles(uri, data):
    """
    Save vehicles information to database
    :param uri: MongoDB Client URI
    :param data: pandas.DataFrame: prepared Vehicle data
    :return: nothing, saving data in db
    """
    if not connection_checker(uri):
        # print("Database currently unavailable. Vehicles save failed")
        # main_logger("error", "Database currently unavailable. Data save to Vehicle table failed")
        raise Exception("Database currently unavailable. Data save to Vehicle table failed")
    client = MongoClient(uri, server_api=ServerApi('1'))
    db_set = client["Poznan"]
    collection = db_set["Vehicles"]
    collection.insert_many(data.to_dict("records"))
    client.close()
