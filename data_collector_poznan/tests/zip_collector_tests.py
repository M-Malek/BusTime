"""
Test zip_collector.py
@M-Malek
"""
import datetime
import sys

from data_collector_poznan.src.gather.zip_gather import schedules_downloader
import shared.tools.env_os_variables as env_variables
from data_collector_poznan.src.parser.zip_collector import SchedulesCollector


def test_one():
    """
    Simple check if function work
    :return:
    """
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
    time5 = datetime.datetime.now()
    line_routes_info, stops, shapes, stop_times = test.prepare_vehicle_data_set()
    print(f"Type of line_routes_info: {type(line_routes_info)}, size: {sys.getsizeof(line_routes_info)}")
    print(f"Type of stops: {type(stops)}, size: {sys.getsizeof(stops)}")
    print(f"Type of shapes: {type(shapes)}, size: {sys.getsizeof(shapes)}")
    print(f"Type of stop_times: {type(stop_times)}, size: {sys.getsizeof(stop_times)}")
    time6 = datetime.datetime.now()
    print(f"Data prepared in time: {time6-time5}")
    print(f"Total data processing time: {time6-time1}")


def test_two():
    """
    Cechk data types:
    :return: Error if data type is wrong
    """
    test_file = schedules_downloader(env_variables.route_archives)
    test = SchedulesCollector(test_file)
    time1 = datetime.datetime.now()
    line_routes_info, stops, shapes, stop_times = test.prepare_vehicle_data_set()
    # line_routes_info_sample = line_routes_info[0]
    # print(line_routes_info_sample)
    print(line_routes_info)
    print("--------------------------")
    print(stops)
    print("--------------------------")
    print(shapes)
    print("--------------------------")
    print(stop_times)
    time2 = datetime.datetime.now()
    print(f"Data preparation time: {time2-time1} s.")
    # assert type(line_routes_info) == "<class 'pandas.core.frame.DataFrame'>", "Wrong data type!"
    # assert type(stops) == "<class 'pandas.core.frame.DataFrame'>", "Wrong data type!"
    # assert type(shapes) == "<class 'pandas.core.frame.DataFrame'>", "Wrong data type!"


# test_one()
test_two()

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
