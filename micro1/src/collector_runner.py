# Libs:
# Global variables
import shared.tools.env_os_variables as env_var
from micro1.src.data_sender import save_vehicles
from micro1.src.data_sender import connection_checker
from micro1.src.feeds_collector import feeds_manager
from shared.tools.log import db_logger


def vehicles():
    # Import data:
    try:
        vehicle_raw_data = feeds_manager(env_var.vehicle_link, env_var.feed_link)
        connection_checker(env_var.db_uri)
        save_vehicles(env_var.db_uri, vehicle_raw_data)
        db_logger(env_var.db_uri, log_type="normal", log_mess="Vehicles positions saved")
    except Exception as e:
        db_logger(env_var.db_uri, log_type="error", log_mess=f"saving data to DataBase: {e}")

