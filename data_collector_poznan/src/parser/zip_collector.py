"""
Prepare downloaded .zip file
@M-Malek
"""
import zipfile
import pandas
import pandas as pd


def schedules_collector(zip_file):
    """
    Decode and read .zip file to create schedule table for db
    :param zip_file: downloaded .zip file with vehicles schedule
    :return:
    """
    # Load data to pandas.Dataframe:
    with zipfile.ZipFile(zip_file).open() as raw_file:
        # Load data from trips.txt:
        with raw_file.open("trips.txt") as raw_trips:
            trip = pd.DataFrame(raw_trips)
            raw_trips.close()

        # Load data from stop_times.txt:
        with raw_file.open('stop_times.txt') as raw_stop_times:
            stop_times = pd.DataFrame(raw_stop_times)
            raw_stop_times.close()

    return trip, stop_times
