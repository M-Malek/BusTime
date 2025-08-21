"""
Main data collecting and parsing logic - works for ZTM Poznań
@M-Malek
"""

# Downloading data:
from data_collector_poznan.src.gather.zip_gather import schedules_downloader
from data_collector_poznan.src.gather.feeds_gater import download_vehicle_data

# Data parsing:
from data_collector_poznan.src.parser.zip_collector import SchedulesCollector
from data_collector_poznan.src.parser.feeds_collector import feeds_manager

# Global variables
import shared.tools.env_os_variables as env_var

# Normal lib:
import time


def vehicles():
    # Import data:
    vehicle_raw_data = download_vehicle_data(env_var.vehicle_link, env_var.feed_link)



def schedules():
    schedules_raw_data = schedules_downloader(env_var.dc_zip_url)
    line_routes_info, stops, shapes, stop_times = SchedulesCollector(schedules_raw_data).prepare_vehicle_data_set()



