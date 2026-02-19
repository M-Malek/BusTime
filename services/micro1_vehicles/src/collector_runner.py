# Libs:
# Global variables
# import shared.tools.env_os_variables as env_var
# from services.micro1_vehicles.src.data_sender import save_vehicles
# from services.micro1_vehicles.src.feeds_collector import feeds_manager
# from services.micro1_vehicles.src.data_sender import db_data_wipeout
# from shared.tools.log_logging import main_logger
# import shared.tools.env_os_variables as env_var
from src.data_sender import save_vehicles
from src.feeds_collector import feeds_manager
from src.data_sender import db_data_wipeout
from src.log_logging import main_logger
import os


def vehicles(client):
    """
    Main vehicles saving function
    :param client: MongoDB Client
    :return: saving data to MongoDB or error
    """
    # Import data:
    try:
        #vehicle_raw_data = feeds_manager(env_var.vehicle_link, env_var.feed_link)  # old version
        vehicle_raw_data = feeds_manager(os.getenv("VEHICLES_URL"), os.getenv("FEED_URL"))  # version for docker
        # connection_checker(env_var.db_uri)
        # save_vehicles(env_var.db_uri, vehicle_raw_data)
        save_vehicles(client, vehicle_raw_data)
        # db_logger(env_var.db_uri, log_type="normal", log_mess="Vehicles positions saved")
        main_logger("info", "Vehicles positions saved!")
    except Exception as e:
        # db_logger(env_var.db_uri, log_type="error", log_mess=f"saving data to DataBase: {e}")
        main_logger("crit", f"Saving vehicles position in Vehicles table in db failed: {e}")
        print(e)


def wipeout():
    """
    Total Vehicle table data wipeout. Use carefully!
    :return: Vehicle table from MongoDB database wipeout
    """
    # main_logger("warning", "Starting to Vehicles table wipeout completed!")
    db_data_wipeout(os.getenv("MONGO_URI"), "Vehicles")  # version vof docker, not docker - change to env_var!
    # main_logger("warning", "Vehicle table wipeout completed!")
