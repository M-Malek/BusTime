"""
Download vehicle positions from MongoDB
@M-Malek
"""
import os

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure
from src.log_logging import main_logger


# Help functions
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
    except ConnectionFailure as e:
        main_logger("error", f"Connection with MongoDB cannot be established: {e}")
        return None
    except Exception as e:
        main_logger("error", f"Error during connection with MongoDB: {e}")
        return None


def db_data_wipeout(client, tables):
    """if not connection_checker(uri):
        # print("Database currently unavailable. Data wipeout failed")
        main_logger("error", "Database currently unavailable. Data wipeout failed")
        return None"""

    # print(f"Starting data wipeout from collections: {tables}")
    main_logger("warning", f"Starting data wipeout from collections: {tables}")
    # client = MongoClient(uri, server_api=ServerApi('1'))
    db_set = client["Poznan"]
    for table in tables:
        # Debug:
        # print(f"{table} type: {type(table)}")
        collection = db_set[table]
        collection.drop()
    # client.close()
    # print(f"Data wipe outed!")
    main_logger("warning", "Data wipe outed!")


def vehicles_data_downloader():
    """
    Download vehicles position data set from MongoDB
    :return: dict with vehicle positions data
    """
    client = connection_establisher(os.getenv("MONGO_URI"))
    if client:
        db_set = client["Poznan"]
        vehicles_data = db_set["Vehicles"]
        #print(vehicles_data)
        # print(client.list_database_names())
        # print(vehicles_data.count_documents({}))
        # for name in client.list_database_names():
        #     print(repr(name))

        ready_data = list(vehicles_data.find({}, {"_id": 0}))
        # ready_data = list(vehicles_data.find({}))
        print(ready_data)
        # db_data_wipeout(client, "Vehicles")
        return ready_data
    else:
        main_logger("error", "Cannot download vehicle data from database")
