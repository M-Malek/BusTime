"""
Test zip_collector.py
@M-Malek
"""
import datetime
from data_collector_poznan.src.parser.zip_collector import schedules_collector, schedules_collector2
from data_collector_poznan.src.gather.zip_gather import schedules_downloader
import shared.tools.env_os_variables as env_variables


def test_one():
    """
    Check file decoding (working on unfinished definition)
    :return: Nothing
    """
    time1 = datetime.datetime.now()
    test_file = schedules_downloader(env_variables.route_archives)
    time2 = datetime.datetime.now()
    print(f"Data downloaded in time: {time2-time1}")
    print("Starting data preparation")
    time3 = datetime.datetime.now()
    # test_data_trips, test_data_times = schedules_collector(test_file)
    # # Print downloaded data
    # print(test_data_times.head(15))
    # print(test_data_trips.head(15))
    test_data = schedules_collector(test_file)
    print(test_data)
    time4 = datetime.datetime.now()
    print(f"Data prepared in {time4-time3}")


def test_two():
    """
    Check file decoding (working on unfinished definition). Works on schedules_collector2()
    :return: Nothing
    """
    time1 = datetime.datetime.now()
    test_file = schedules_downloader(env_variables.route_archives)
    time2 = datetime.datetime.now()
    print(f"Data downloaded in time: {time2-time1}")
    print("Starting data preparation")
    time3 = datetime.datetime.now()
    # test_data_trips, test_data_times = schedules_collector(test_file)
    # # Print downloaded data
    # print(test_data_times.head(15))
    # print(test_data_trips.head(15))
    test_data = schedules_collector2(test_file)
    print(test_data)
    time4 = datetime.datetime.now()
    print(f"Data prepared in {time4-time3}")


def test_tree():
    from data_collector_poznan.src.parser.zip_collector import SchedulesCollector
    time1 = datetime.datetime.now()
    test_file = schedules_downloader(env_variables.route_archives)
    time2 = datetime.datetime.now()
    print(f"Data downloaded in time: {time2 - time1}")
    print("Starting data preparation")
    time3 = datetime.datetime.now()
    test = SchedulesCollector(test_file)
    test.data_presentation()
    time4 = datetime.datetime.now()
    print(f"Data to pandas Dataframe in {time4-time3}")
    stops = test.stops_locations
    print(stops.head(10))


def test_four():
    from data_collector_poznan.src.parser.zip_collector import SchedulesCollector
    time1 = datetime.datetime.now()
    test_file = schedules_downloader(env_variables.route_archives)
    time2 = datetime.datetime.now()
    print(f"Data downloaded in time: {time2 - time1}")
    print("Starting data preparation")
    time3 = datetime.datetime.now()
    test = SchedulesCollector(test_file)
    time4 = datetime.datetime.now()
    # test.data_presentation()
    print(f"Data to pandas Dataframe in {time4-time3}")
    stops = test.stops_locations
    trips = test.trips
    print(trips.head(10))
    # print(stops.head(10))
    # basic_info = test.load_basic_information()
    # print(basic_info.head(10))


# test_one()
# test_two()
# test_tree()
test_four()

"""
Founded errors:
test_one():
-----------------------
File "zip_gather.py", line 76, in schedules_downloader
    response = requests.get()
TypeError: get() missing 1 required positional argument: 'url'
Typo corrected
----------------------
  File "zipfile.py", line 264, in _EndRecData
    fpin.seek(0, 2)
AttributeError: 'Response' object has no attribute 'seek'
Incorrect variable type - function need response.content, not response itself. Corrected on response.content 
  File "zip_collector.py", line 17, in schedules_collector
    with zipfile.ZipFile(zip_file).open() as raw_file:
TypeError: ZipFile.open() missing 1 required positional argument: 'name'
Added name parameter
  File "zipfile.py", line 264, in _EndRecData
    fpin.seek(0, 2)
AttributeError: 'Response' object has no attribute 'seek'
with zipfile.ZipFile(zip_file).open(io.BytesIO(zip_file)) in zip_collector.py -> if zipfile.ZipFile loads a zip,
why opened it again? Replaced on with zipfile.ZipFile(zip_file)
----------------------
Incorrect encoding: no Polish letters! Repaired by changing encoding!
"""
