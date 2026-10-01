from ztm_tools.mongo_tools.mongo_connect import create_mongo_connection
from ztm_tools.logging.logger import main_logger
from os import getenv

def collect_stop_position(stop_id):
    con = create_mongo_connection(getenv("MONGO_URI"))
    col = con["Poznan"]["Stops"]
    if type(stop_id) is not str or type(stop_id) is not int:
        if type(stop_id) is list:
            stop_id = int(stop_id[0])
        if type(stop_id) is dict:
            main_logger("error", f"collect_stop_position: stop_id {stop_id} is dict!")
            return None, None
    else:
        if type(stop_id) is int:
            pass
        else:
            stop_id = int(stop_id)
    try:
        searched_stop = col.find_one({"stop_id": stop_id})
        lat = searched_stop["lat"]
        lng = searched_stop["lng"]
        return lat, lng
    except Exception:
        return None, None