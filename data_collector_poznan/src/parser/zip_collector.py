"""
Prepare downloaded .zip file
@M-Malek
"""
import zipfile
import pandas
import pandas as pd
import io


def schedules_collector(zip_file):
    """
    Decode and read .zip file to create schedule table for db
    :param zip_file: downloaded .zip file with vehicles schedule
    :return:
    """
    # Load data to pandas.Dataframe:
    with zipfile.ZipFile(zip_file) as raw_file:
        # Load data from trips.txt:
        with raw_file.open("trips.txt") as raw_trips:
            trips = pd.read_csv(raw_trips, encoding="utf-8-sig")
            raw_trips.close()

        # Load data from stop_times.txt:
        with raw_file.open('stop_times.txt') as raw_stop_times:
            stop_times = pd.read_csv(raw_stop_times, encoding="utf-8-sig")
            raw_stop_times.close()

        # Load data from shapes.txt:
        with raw_file.open('shapes.txt') as raw_shapes:
            shapes = pd.read_csv(raw_shapes, encoding="utf-8-sig")
            raw_shapes.close()

        # Load data from shapes.txt:
        with raw_file.open('stops.txt') as raw_stops:
            stops = pd.read_csv(raw_stops, encoding="utf-8-sig")
            raw_stops.close()

    # Create result list:
    result = []

    # Prepare data:
    for route_id in trips['route_id'].unique():
        route_trips = trips[trips['route_id'] == route_id]

    return trips, stop_times
