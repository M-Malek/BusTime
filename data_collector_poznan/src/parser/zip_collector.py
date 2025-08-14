"""
Prepare downloaded .zip file
@M-Malek
"""
import zipfile
import pandas
import pandas as pd
import io
import logging


def schedules_collector(zip_file):
    """
    Decode and read .zip file to create schedule table for db
    :param zip_file: downloaded .zip file with vehicles schedule
    :return:
    """
    # Load data to pandas.Dataframe:
    # Debug:
    print("Starting read data from .zip")
    with zipfile.ZipFile(zip_file) as raw_file:
        # Load data from trips.txt:
        # with raw_file.open("trips.txt") as raw_trips:
        #     trips = pd.read_csv(raw_trips, encoding="utf-8-sig")
        #     raw_trips.close()
        trips = pd.read_csv(raw_file.open("trips.txt", encoding="utf-8-sig"))

        # Load data from stop_times.txt:
        # with raw_file.open('stop_times.txt') as raw_stop_times:
        #     stop_times = pd.read_csv(raw_stop_times, encoding="utf-8-sig")
        #     raw_stop_times.close()
        stop_times = pd.read_csv(raw_file.open("stop_times.txt", encoding="utf-8-sig"))

        # Load data from shapes.txt:
        # with raw_file.open('shapes.txt') as raw_shapes:
        #     shapes = pd.read_csv(raw_shapes, encoding="utf-8-sig")
        #     raw_shapes.close()
        shapes = pd.read_csv(raw_file.open("shapes.txt", encoding="utf-8-sig"))

        # Load data from shapes.txt:
        # with raw_file.open('stops.txt') as raw_stops:
        #     stops = pd.read_csv(raw_stops, encoding="utf-8-sig")
        #     raw_stops.close()
        stops = pd.read_csv(raw_file.open("stops.txt", encoding="utf-8-sig"))

    # Debug:
    print("Data from .zip read!")
    # Create result list:
    result = []

    # Prepare data:
    # Debug
    print("Start preparing data")
    for route_id in trips['route_id'].unique():
        route_trips = trips[trips['route_id'] == route_id]

        # Debug:
        print("Route_trips prepared")
        # print(route_trips.head(10))

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
                # print(stop_data)

            trip_data = {
                "route_id": str(route_id),
                "trip_id": trip_id,
                "shape_id": shape_id,
                "direction_id": int(direction_id),
                "stops": ready_stops
            }
            result.append(trip_data)

    return result


def schedules_collector2(zip_file):
    logging.basicConfig(level=logging.INFO)

    with zipfile.ZipFile(zip_file) as raw_file:
        trips = pd.read_csv(raw_file.open("trips.txt"), encoding="utf-8-sig")
        stop_times = pd.read_csv(raw_file.open("stop_times.txt"), encoding="utf-8-sig")
        stops = pd.read_csv(raw_file.open("stops.txt"), encoding="utf-8-sig")

    stops_dict = stops.set_index('stop_id').to_dict('index')
    result = []

    for route_id, route_trips in trips.groupby('route_id'):
        for trip in route_trips.itertuples(index=False):
            trip_id = trip.trip_id
            shape_id = trip.shape_id
            direction_id = trip.direction_id

            trip_stops = stop_times[stop_times['trip_id'] == trip_id].sort_values('stop_sequence')

            ready_stops = []
            for stop_time in trip_stops.itertuples(index=False):
                stop_info = stops_dict[stop_time.stop_id]
                ready_stops.append({
                    "stop_id": stop_time.stop_id,
                    "stop_name": stop_info['stop_name'],
                    "departure_time": stop_time.departure_time,
                    "stop_sequence": int(stop_time.stop_sequence),
                    "location": {
                        "lat": float(stop_info['stop_lat']),
                        "lng": float(stop_info['stop_lon'])
                    }
                })

            result.append({
                "route_id": route_id,
                "trip_id": trip_id,
                "shape_id": shape_id,
                "direction_id": int(direction_id),
                "stops": ready_stops
            })

    return result


class SchedulesCollector:
    def __init__(self, zip_file):
        # Load raw data
        with zipfile.ZipFile(zip_file) as raw_file:
            self.trips = pd.read_csv(raw_file.open("trips.txt"), encoding="utf-8-sig", sep=',')
            self.stop_times = pd.read_csv(raw_file.open("stop_times.txt"), encoding="utf-8-sig", sep=',')
            self.stops = pd.read_csv(raw_file.open("stops.txt"), encoding="utf-8-sig", sep=',')
            raw_file.close()

        # Debug:
        print(f"Trips: {type(self.trips)}")
        print(f"Stops: {type(self.stops)}")
        print(f"Stop_times: {type(self.stop_times)}")

        # Save prepared data:
        self.stops_locations = self.load_stops()
        self.basic_information = self.load_basic_information()
        self.vehicle_times = self.load_stop_times()

        self.trips = self.load_basic_information()

    def data_presentation(self):
        """
        For debug: check downloaded data
        :return:
        """
        print("Trips:")
        print(self.trips.head(10))
        print("Stop times:")
        print(self.stop_times.head(10))
        print("Stops:")
        print(self.stops.head(10))

    def load_stops(self):
        """
        Prepare file "stops.txt" by extracting the appropriate data
        :return: pandas.DataFrame with data: stop_id, short_name, stop_name, latitude and longitude
        """
        # return self.stops[self.stops.columns[:-1]]
        return self.stops.drop(["stop_code"], axis=1)

    def load_basic_information(self):
        """
        Prepare file "trips.txt" by extracting the appropriate data
        :return: pandas.DataFrame with data: route_id, trip_id, shape_id, direction_id
        """
        return self.trips.drop(["route_id", "trip_headsign", "brigade"], axis=1)

    def load_stop_times(self):
        """
        Prepare file "stop_times.txt" by extracting the appropriate data
        :return: pandas.DataFrame with data:
        """
        return self.stop_times.drop(["pickup_type", "drop_off_type"], axis=1)

    def prepare_vehicle_data_set(self):
        pass

