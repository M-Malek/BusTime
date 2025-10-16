"""
Main data collecting and parsing logic - works for ZTM Poznań
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
from shared.tools.log import log

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


def main():
    """
    Main data saver program loop
    :return:
    """
    # Starting internal variables
    # Hour to check changes in timetable:
    # 4:00, 8:00, 12:00, 16:00, 20:00,
    timetable_times_check = [(datetime.strptime("04:00", "%H:%M").time(), datetime.strptime("04:05", "%H:%M").time()),
                             (datetime.strptime("08:00", "%H:%M").time(), datetime.strptime("08:05", "%H:%M").time()),
                             (datetime.strptime("12:00", "%H:%M").time(), datetime.strptime("12:05", "%H:%M").time()),
                             (datetime.strptime("16:00", "%H:%M").time(), datetime.strptime("16:05", "%H:%M").time()),
                             (datetime.strptime("19:45", "%H:%M").time(), datetime.strptime("20:05", "%H:%M").time()),
                             ]
    timetable_checked = False
    while True:
        current_time = datetime.now().time()
        # print(f"Time now: {current_time}")
        for time_set in timetable_times_check:
            # Add brake after saving data when an hour has been caught!
            if in_time_period(time_set[0], time_set[1], current_time):
                print("Time in time period")
                if not timetable_checked:
                    schedules()
                    log()
                    # print("Timetable ont checked!")
                    timetable_checked = True
            else:
                log(message_type=2)
                timetable_checked = False

        time.sleep(60)


if __name__ == "__main__":
    main()



