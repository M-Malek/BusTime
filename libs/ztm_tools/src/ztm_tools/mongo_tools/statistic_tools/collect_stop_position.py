from ztm_tools.mongo_tools.mongo_connect import create_mongo_connection
from os import getenv

def collect_stop_position(stop_id):
    con = create_mongo_connection(getenv("MONGO_URI"))
    col = con["Poznan"]["Stops"]
    try:
        searched_stop = col.find_one({"stop_id": stop_id})
        lat = searched_stop["lat"]
        lng = searched_stop["lng"]
        return lat, lng
    except Exception:
        return None, None