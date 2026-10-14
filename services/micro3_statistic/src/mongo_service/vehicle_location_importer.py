"""
Download vehicle positions from MongoDB
@M-Malek
"""
import os

import pymongo
from ztm_tools.mongo_tools.mongo_connect import create_mongo_connection
from ztm_tools.logging.logger import main_logger

def vehicles_data_downloader(batch_count=1000):
    """
    Iterate through MongoDB and download vehicles position data set from MongoDB
    :param batch_count: Number of batches to download
    :return: dict with vehicle positions data
    """

    client = create_mongo_connection(os.getenv("MONGO_URI"))
    if client is None:
        main_logger("error", "Cannot download vehicle data from database")
        return iter(())

    def iter_mongo_documents():
        try:
            collection = client["Poznan"]["Vehicles"]
            cursor = (
                collection.find({}, {"_id": 0})
                .sort([("route_id", 1), ("trip_id", 1)])
                .allow_disk_use(True)
                .batch_size(batch_count)
            )

            yield from cursor

        except pymongo.errors.PyMongoError as err:
            main_logger("error", f"Error during preparing data in batch: {err}")

        finally:
            client.close()

    return iter_mongo_documents()

# def vehicles_data_downloader(batch_count=5000):
#     """
#     Iterate through MongoDB and download vehicles position data set from MongoDB
#     :param batch_count: Number of batches to download
#     :return: dict with vehicle positions data
#     """
#     client = create_mongo_connection(os.getenv("MONGO_URI"))
#
#     if client:
#         db_set = client["Poznan"]
#         vehicles_data = db_set["Vehicles"]
#         #print(vehicles_data)
#         # print(client.list_database_names())
#         # print(vehicles_data.count_documents({}))
#         # for name in client.list_database_names():
#         #     print(repr(name))
#
#         data = vehicles_data.find({}, {"_id": 0})
#         # ready_data = list(vehicles_data.find({}))
#         client.close()
#         return data
#     else:
#         main_logger("error", "Cannot download vehicle data from database")
#         return None
