import os

import pymongo
from ztm_tools.mongo_tools.mongo_connect import create_mongo_connection
from ztm_tools.logging.logger import main_logger

def mongo_iter_downloader(collection, subcollection, batch_count=1000):
    """
    Iterate through MongoDB and download vehicles position data set from MongoDB
    :param collection: main mongo collection name
    :param subcollection: subcollection name
    :param batch_count: Number of batches to download
    :return: dict with vehicle positions data
    """

    client = create_mongo_connection(os.getenv("MONGO_URI"))
    if client is None:
        main_logger("error", "Cannot download vehicle data from database")
        return iter(())

    def iter_mongo_documents(collection=collection, subcollection=subcollection):
        try:
            collection = client[collection][subcollection]
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