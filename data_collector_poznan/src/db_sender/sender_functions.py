"""
Sender functions for main.py
@M-Malek
"""
# Downloading data:
from datetime import datetime
import time

from data_collector_poznan.src.gather.zip_gather import schedules_downloader

# Data parsing:
from data_collector_poznan.src.parser.zip_collector import SchedulesCollector
from data_collector_poznan.src.parser.feeds_collector import feeds_manager

# Global variables
import shared.tools.env_os_variables as env_var

# Toolbox
from shared.tools.filestoolbox import in_time_period

# Data to db saving:
from data_collector_poznan.src.db_sender.data_sender import connection_checker, save_vehicles
from data_collector_poznan.src.db_sender.data_sender import save_timetables, save_stops
from data_collector_poznan.src.db_sender.data_sender import save_data


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


def save_data_in_db(with_wipeout=False):
    schedules_raw_data = schedules_downloader(env_var.dc_zip_url)
    if with_wipeout:
        line_routes_info, shapes, stop_times = SchedulesCollector(schedules_raw_data).prepare_vehicle_data_set2()
        save_data(env_var.db_uri, line_routes_info, shapes, stop_times, with_wipeout=True)
    else:
        line_routes_info, shapes, stop_times = SchedulesCollector(schedules_raw_data).prepare_vehicle_data_set2()
        save_data(env_var.db_uri, line_routes_info, shapes, stop_times)

