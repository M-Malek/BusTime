"""
Main data collecting and parsing logic - works for ZTM Poznań
@M-Malek
"""

# Downloading data:
import datetime
import time

from data_collector_poznan.src.gather.zip_gather import schedules_downloader

# Data parsing:
from data_collector_poznan.src.parser.zip_collector import SchedulesCollector
from data_collector_poznan.src.parser.feeds_collector import feeds_manager

# Global variables
import shared.tools.env_os_variables as env_var

# Normal lib:
import time

# Data to db saving:
from data_collector_poznan.src.db_sender.data_sender import connection_checker, save_vehicles
from data_collector_poznan.src.db_sender.data_sender import save_timetables, save_stops


def vehicles():
    # Import data:
    vehicle_raw_data = feeds_manager(env_var.vehicle_link, env_var.feed_link)
    connection_checker()
    save_vehicles(env_var.db_uri, vehicle_raw_data)


def schedules():
    schedules_raw_data = schedules_downloader(env_var.dc_zip_url)
    line_routes_info, shapes, stop_times = SchedulesCollector(schedules_raw_data).prepare_vehicle_data_set()
    # Add checker if data need to be replaced!!!
    save_timetables(env_var.db_uri, line_routes_info, shapes, stop_times)


def stops():
    schedules_raw_data = schedules_downloader(env_var.dc_zip_url)
    stops_data = SchedulesCollector(schedules_raw_data).stops
    save_stops(env_var.db_uri, stops_data)


def log():
    pass


def main():
    """
    Main data saver program loop
    :return:
    """
    hours = ["4:00", "8:00", "12:00", "16:00", "20:00", "24:00"]  # hours when vehicles stop times are checked
    while True:
        current_time = datetime.datetime.now()
        actual_hour = str(current_time.hour) + ":" + str(current_time.minute)
        if actual_hour in hours:

        time.sleep(60)


if __name__ == "__main__":
    main()



