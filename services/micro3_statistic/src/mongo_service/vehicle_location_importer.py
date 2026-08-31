"""
Download vehicle positions from MongoDB
@M-Malek
"""
import os

from ztm_tools.mongo_tools.mongo_connect import create_mongo_connection
from ztm_tools.logging.logger import main_logger

def vehicles_data_downloader():
    """
    Download vehicles position data set from MongoDB
    :return: dict with vehicle positions data
    """
    client = create_mongo_connection(os.getenv("MONGO_URI"))
    if client:
        db_set = client["Poznan"]
        vehicles_data = db_set["Vehicles"]
        #print(vehicles_data)
        # print(client.list_database_names())
        # print(vehicles_data.count_documents({}))
        # for name in client.list_database_names():
        #     print(repr(name))

        data = vehicles_data.find({}, {"_id": 0})
        # ready_data = list(vehicles_data.find({}))

        return data
    else:
        main_logger("error", "Cannot download vehicle data from database")
        return None
