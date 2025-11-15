import datetime

from data_collector_poznan.src.db_sender.data_sender import save_timetables
from data_collector_poznan.src.db_sender.sender_functions import schedules
from data_collector_poznan.src.db_sender.sender_functions import save_data_in_db


# Test 1: try connection to data_server
def sender_test_1():
    """
    Test connection to data server
    :return: Log "Connection successfully achieved!" if connection was successfully.
    """
    schedules()


def sender_test_2():
    """
    Check if it even connects and save something in db
    :return: Log "Data saved" if works else error
    """
    time1 = datetime.datetime.now()
    save_data_in_db()
    time2 = datetime.datetime.now()
    print(f"Test completed, data saving time: {time2-time1}")
    # Function sender_test2 running time: 3 minutes 3 seconds


def sender_test_3():
    """
    Connect to db, wipe all data saved in collections Stop_times, Trips and Shapes, save new data
    :return: Log "Data saved" if works else error
    """
    time1 = datetime.datetime.now()
    save_data_in_db(with_wipeout=True)
    time2 = datetime.datetime.now()
    print(f"Test completed, data saving time: {time2-time1}")
    # Function sender_test2 running time: 3 minutes 3 seconds


# sender_test_1()
# sender_test_2()
sender_test_3()

"""
Tests result:
No. 1 - ok
No. 2 - ok
No. 3 - 
"""
# data_sender do przeróbki tak by nie było typów NumPy - przerobiony na zapis wszystkich danych, potem wyjmie się te
# potrzebne
