"""Check if Stops collection in MongoDB has data"""
from ztm_tools.mongo_tools.mongo_connect import create_mongo_connection
from ztm_tools.mongo_tools.check_collection import check_collection
import os


def check_stops_collection():
    """Check if Stops collection in MongoDB has data"""
    client = create_mongo_connection(os.getenv("MONGO_URI"))
    db_set = client["Poznan"]
    all_sets = db_set.list_collection_names()
    if "Stops" in all_sets:
        return check_collection(db_set["Stops"])
    else:
        return "No Stops collection in MongoDB"

