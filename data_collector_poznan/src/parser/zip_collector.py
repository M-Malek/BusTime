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

        for _, trip in route_trips.iterrows():
            trip_id = trip['trip_id']
            shape_id = trip['shape_id']
            direction_id = trip['direction_id']

            # Pobieranie przystanków dla danego trip_id
            trip_stops = stop_times[stop_times['trip_id'] == trip_id].sort_values('stop_sequence')

            ready_stops = []
            for _, stop_time in trip_stops.iterrows():
                stop_id = stop_time['stop_id']
                stop_info = stops[stops['stop_id'] == stop_id].iloc[0]

                stop_data = {
                    "stop_id": stop_id,
                    "stop_name": stop_info['stop_name'],
                    "departure_time": stop_time['departure_time'],
                    "stop_sequence": int(stop_time['stop_sequence']),
                    "location": {
                        "lat": float(stop_info['stop_lat']),
                        "lng": float(stop_info['stop_lon'])
                    }
                }
                ready_stops.append(stop_data)

            trip_data = {
                "route_id": str(route_id),
                "trip_id": trip_id,
                "shape_id": shape_id,
                "direction_id": int(direction_id),
                "stops": stops
            }
            result.append(trip_data)

    return result
