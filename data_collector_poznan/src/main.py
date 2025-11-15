"""
Main data collecting and parsing logic - works for ZTM Poznań
@M-Malek
"""

# Sender functions
from data_collector_poznan.src.db_sender.sender_functions import vehicles, schedules, stops

# Toolbox
from shared.tools.filestoolbox import in_time_period
from shared.tools.log import log

# Normal lib:
import time
import datetime

# Data to db saving:
from data_collector_poznan.src.db_sender.data_sender import connection_checker, save_vehicles
from data_collector_poznan.src.db_sender.data_sender import save_timetables, save_stops


async def timetables_main():
    pass


async def vehicles_main():
    pass


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
                             (datetime.strptime("19:22", "%H:%M").time(), datetime.strptime("19:25", "%H:%M").time()),
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




