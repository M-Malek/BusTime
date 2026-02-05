"""
Parse downloaded and readed .zip file
@M-Malek
"""
import datetime

from services.micro2_timetables.src.zip_reader import ZIPReader
from services.micro2_timetables.src.zip_gather import zip_downloading

import pandas as pd
from pandas import merge


class StopTime:
    def __init__(self, stop_id, arv_time, dep_time, seq, pickup, dropoff):
        self.stop_id = stop_id
        self.arv_time = arv_time
        self.dep_time = dep_time
        self.seq = seq
        self.pickup = pickup
        self.dropoff = dropoff

    def to_dict(self) -> dict:
        return {
            "seq": self.seq,
            "stop_id": self.stop_id,
            "arv_time": self.arv_time,
            "dep_time": self.dep_time,
            "pickup": self.pickup,
            "dropoff": self.dropoff
        }


class Shape:
    def __init__(self, seq, lat, lon):
        self.sequence = seq
        self.latitude = lat
        self.longitude = lon

    def to_dict(self) -> dict:
        return {
            "sequence": self.sequence,
            "latitude": self.latitude,
            "longitude": self.longitude
        }


class Route:
    def __init__(self, route_id, stop_times, shape):
        self.route_id = route_id
        self.stop_times = stop_times
        self.shape = shape

    def to_dict(self) -> dict:
        return {
            "route_id": self.route_id,
            "stops": self.stop_times,
            "shape": self.shape,
        }


class Line:
    def __init__(self, number, agency, color):
        self.line_number = number
        self.agency = agency
        self.color = color
        self.routes = {}

    def to_dict(self) -> dict:
        return {
            "line_number": self.line_number,
            "agency": self.agency,
            "line_color": self.color,
            "routes": self.routes
        }


def zip_parser(url_raw_data_set):
    """
    Main .zip parser file - open
    :param url_raw_data_set:
    :return:
    """
    # Imports:
    from time import perf_counter

    # Help functions:
    def build_stop_times(trip_id):
        if trip_id in stop_time_cache:
            return stop_time_cache[trip_id]

        time_rows = times_by_trip.get_group(trip_id)
        stop_times = []

        for t in time_rows.itertuples(index=False):
            stop_times.append(
                StopTime(
                    int(t.stop_id),
                    str(t.arrival_time),
                    str(t.departure_time),
                    int(t.stop_sequence),
                    int(t.pickup_type),
                    int(t.drop_off_type),
                ).to_dict()
            )

        stop_time_cache[trip_id] = stop_times
        return stop_times

    # From other scopes
    raw_zip = zip_downloading(url_raw_data_set)
    raw_data_set = ZIPReader(raw_zip)

    # Basic vehicle information: line number, agency, color
    # Step 1: reading all lines:
    # basic_line_info - describes basic information about the line
    basic_line_info = raw_data_set.routes[["route_id", "agency_id", 'route_color', "route_type"]]

    # basic_trip_info - basic information's about trips
    basic_trip_info = raw_data_set.trips[["route_id", "trip_id", "service_id", "shape_id"]]

    # Loop to finding shape set and route set
    # Find all unique sets: route_id, trip_id, shape_id
    searching_set = basic_trip_info[["route_id", "trip_id", "shape_id"]]

    # Find all unique line numbers
    lines = basic_trip_info["route_id"].unique()

    # Find all shapes and all times data
    # all_shapes = raw_data_set.shapes
    all_times = raw_data_set.stop_times

    # Group all necessary information:
    trip_info_by_route = basic_trip_info.groupby("route_id")
    # shapes_by_id = all_shapes.groupby("shape_id")
    times_by_trip = all_times.groupby("trip_id")
    searching_by_route = searching_set.groupby("route_id")

    # Fast access by route_id
    line_info_by_route = basic_line_info.set_index("route_id")

    # Create cache files
    shape_cache = {}
    stop_time_cache = {}

    # Debug - time measurments
    # t0 = perf_counter()

    ready_lines = {}

    for line in lines:
        # --- Jedno pobranie danych dla linii (krok 1,5) ---
        route_trip_info = trip_info_by_route.get_group(line)
        route_searching = searching_by_route.get_group(line)
        line_info = line_info_by_route.loc[line]

        # --- Unique shape_id and trip_id ---
        # unique_shapes = route_trip_info["shape_id"].unique()
        unique_trips = route_trip_info["trip_id"].unique()

        # --- Building shapes  ---
        # shapes_by_shape_id = {
        #     int(shape_id): build_shape(int(shape_id))
        #     for shape_id in unique_shapes
        # }

        # --- Building stop_times(krok 2,3) ---
        stop_times_by_trip = {
            str(trip_id): build_stop_times(str(trip_id))
            for trip_id in unique_trips
        }

        # --- Route assembling ---
        routes = {}

        for row in route_searching.itertuples(index=False):
            trip_id = str(row.trip_id)
            shape_id = int(row.shape_id)

            routes[trip_id] = {
                "trip_id": trip_id,
                "shape_id": shape_id,
                "trip_data": stop_times_by_trip[trip_id],
                # "shape_data": shapes_by_shape_id[shape_id],
            }

        # --- Typ pojazdu (krok 5) ---
        vehicle_type = "tram" if int(line_info.route_type) == 0 else "bus"

        # --- Finalny zapis linii ---
        ready_lines[line] = {
            "line_number": str(line),
            "type": vehicle_type,
            "agency": int(line_info.agency_id),
            "line_color": str(line_info.route_color),
            "routes": routes,
        }

    # print(f"Czas opracowania danych pojazdów: {perf_counter() - t0:.2f}s")
    return ready_lines

