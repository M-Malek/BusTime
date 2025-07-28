"""
Test zip_colletor.py
@M-Malek
"""
import datetime
from data_collector_poznan.src.parser.zip_collector import schedules_collector
from data_collector_poznan.src.gather.zip_gather import schedules_downloader
import shared.tools.env_os_variables as env_variables


def test_one():
    """
    Check file decoding (working on unfinished definition)
    :return: Nothing
    """
    time1 = datetime.datetime.now()
    test_file = schedules_downloader(env_variables.route_archives)
    test_data_trips, test_data_times = schedules_collector(test_file)
    # Print downloaded data


test_one()
