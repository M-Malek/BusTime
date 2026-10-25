from ztm_tools.mongo_tools.mongo_connect import create_mongo_connection
from ztm_tools.logging.logger import main_logger
from os import getenv

def collect_stop_position(stop_id):
    """
    Download data of stop position for given stop id_
    :param stop_id:
    :return:
    """
    # Check if stop_id is an int! If isn't: we cannot download data
    if type(stop_id) is not int:
        if type(stop_id) is str:
            stop_id = int(stop_id)
        elif type(stop_id) is list:
            stop_id = int(stop_id[0])
        else:
            if type(stop_id) is dict:
                main_logger("error", f"collect_stop_position: stop_id {stop_id} is dict!")
                return None, None
            else:
                main_logger(f"error", f"collect_stop_position: stop_id {stop_id} is "
                                      f"not understandable for function!")
                return None, None

    con = create_mongo_connection(getenv("MONGO_URI"))
    col = con["Poznan"]["Stops"]

    try:
        searched_stop = col.find_one({"stop_id": stop_id})
        lat = searched_stop["lat"]
        lng = searched_stop["lng"]
        con.close()
        return lat, lng
    except Exception as e:
        main_logger("error", f"collect_stop_position: An error occured! {e}\n. Returning None.")
        con.close()
        return None, None