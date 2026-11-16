"""
Download vehicle positions from MongoDB
@M-Malek
"""
import os

from ztm_tools.mongo_tools.mongo_connect import create_mongo_connection
from src.mongo_service.mongo_iter_downloader import mongo_iter_downloader

def vehicle_trip_keys():
    """Return distinct (trip_id, route_id) keys currently present in Vehicles."""
    client = create_mongo_connection(os.getenv("MONGO_URI"))
    if client is None:
        return []
    try:
        collection = client["Poznan"]["Vehicles"]
        return list(collection.aggregate([
            {"$match": {"trip_id": {"$exists": True}, "route_id": {"$exists": True}}},
            {"$group": {"_id": {"trip_id": "$trip_id", "route_id": "$route_id"}}},
        ]))
    finally:
        client.close()


def delete_processed_vehicle_documents(document_ids):
    """Delete source rows only after their results have been saved."""
    if not document_ids:
        return 0
    client = create_mongo_connection(os.getenv("MONGO_URI"))
    if client is None:
        raise ConnectionError("Cannot connect to MongoDB to clean processed Vehicles")
    try:
        result = client["Poznan"]["Vehicles"].delete_many({"_id": {"$in": document_ids}})
        return result.deleted_count
    finally:
        client.close()


def vehicles_data_downloader(
    trip_id, route_id, last_timestamp=None, last_id=None, batch_count=1000
):
    """
    Iterate through MongoDB and download vehicles position data set from MongoDB
    :param batch_count: Number of batches to download
    :return: iterator of new vehicle position documents, including _id
    """
    query = {"trip_id": trip_id, "route_id": route_id}
    if last_timestamp is not None and last_id is not None:
        query["$or"] = [
            {"timestamp": {"$gt": last_timestamp}},
            {"timestamp": last_timestamp, "_id": {"$gt": last_id}},
        ]
    elif last_timestamp is not None:
        query["timestamp"] = {"$gt": last_timestamp}
    return mongo_iter_downloader(
        "Poznan", "Vehicles", batch_count, query=query,
        sort=[("timestamp", 1), ("_id", 1)],
    )
    # client = create_mongo_connection(os.getenv("MONGO_URI"))
    # if client is None:
    #     main_logger("error", "Cannot download vehicle data from database")
    #     return iter(())
    #
    # def iter_mongo_documents():
    #     try:
    #         collection = client["Poznan"]["Vehicles"]
    #         cursor = (
    #             collection.find({}, {"_id": 0})
    #             .sort([("route_id", 1), ("trip_id", 1)])
    #             .allow_disk_use(True)
    #             .batch_size(batch_count)
    #         )
    #
    #         yield from cursor
    #
    #     except pymongo.errors.PyMongoError as err:
    #         main_logger("error", f"Error during preparing data in batch: {err}")
    #
    #     finally:
    #         client.close()
    #
    # return iter_mongo_documents()

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
