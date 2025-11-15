"""
Prepare downloaded .zip file
@M-Malek
"""
import datetime
import zipfile
import pandas
import pandas as pd
import io
import logging


class SchedulesCollector:
    def __init__(self, zip_file):
        # Load raw data
        with zipfile.ZipFile(zip_file) as raw_file:
            # Files needed to being preprocessed before use:
            self.trips = pd.read_csv(raw_file.open("trips.txt"), encoding="utf-8-sig", sep=',')
            self.stop_times = pd.read_csv(raw_file.open("stop_times.txt"), encoding="utf-8-sig", sep=',')
            self.stops = pd.read_csv(raw_file.open("stops.txt"), encoding="utf-8-sig", sep=',')
            # Files needed to import without changes
            self.shapes = pd.read_csv(raw_file.open("shapes.txt"), encoding="utf-8-sig", sep=',')
            raw_file.close()

        # Debug:
        # print(f"Trips: {type(self.trips)}")
        # print(f"Stops: {type(self.stops)}")
        # print(f"Stop_times: {type(self.stop_times)}")

        # Prepare data for files which need tobe prepared:
        # self.trips = self.load_basic_information()
        # self.stop_times = self.load_stop_times()
        # self.stops = self.load_stops()

    def load_data_for_adv_data_prep(self):
        """
        Prepare data for files which need to be prepared:
        :return: None
        """
        self.trips = self.load_basic_information()
        self.stop_times = self.load_stop_times()
        self.stops = self.load_stops()

    def data_presentation(self):
        """
        For debug: check downloaded data
        :return: None
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
        return self.trips.drop(["brigade"], axis=1)

    def load_stop_times(self):
        """
        Prepare file "stop_times.txt" by extracting the appropriate data
        :return: pandas.DataFrame with data:
        """
        return self.stop_times.drop(["pickup_type", "drop_off_type"], axis=1)

    def prepare_vehicle_data_set(self, with_stops=False):
        """
        Prepare dataset with all necessary information for all routes
        :return: four datasets as pandas DataFrame
        """
        # 1. Prepare set of basic information's:
        # line (service_id) number: shape_id (route identifier)
        self.load_data_for_adv_data_prep()
        line_routes_info = (
            self.trips.groupby("service_id")
                .apply(lambda g: [
                {"shape_id": sid, "trips": list(sub["trip_id"])}
                for sid, sub in g.sort_values(["shape_id", "trip_id"], kind="stable")
                       .groupby("shape_id")
            ])
                .reset_index()
                .rename(columns={"service_id": "service_id", 0: "lines"})
        )
        # print(line_routes_info)

        # 2. Prepare shapes information's:
        # for each shape create a set of data: stop sequence number,his longitude and latitude
        # Grouping shapes by shape_id gives us ready set of data
        # shapes = (self.shapes.groupby("shape_id").apply(
        #     lambda g: g[["shape_pt_lat", "shape_pt_lon", "shape_pt_sequence"]].to_dict(orient="records").to_dict()
        # ).rename(columns={"shape_pt_lat": "shape_lat", "shape_pt_lon": "shape_lng", "shape_pt_sequence": "seq"})
        # )
        shapes_dict = {}
        for shape_id, group in self.shapes.groupby("shape_id"):
            shapes_dict[shape_id] = {
                int(row["shape_pt_sequence"]): [row["shape_pt_lat"], row["shape_pt_lon"]]
                for _, row in group.iterrows()
            }

        shapes = pd.DataFrame(list(shapes_dict.items()), columns=["shape_id", "route"])
        # Debug:
        # for shape_id, group in shapes:
        #     print(f"--- {shape_id} ---")
        #     print(group.head())

        # 3. Prepare stops information's: prepared when data has been downloaded

        # 4. Prepare stops times information's:
        # Grouping stop times by trip_id gives us ready set of data
        # stop_times = self.stop_times.groupby("trip_id")
        stop_times_dict = {}
        for trip_id, group in self.stop_times.groupby("trip_id"):
            stop_times_dict[trip_id] = {
                int(row["stop_sequence"]): [str(row["arrival_time"]),
                                            str(row["departure_time"]),
                                            int(row["stop_id"])]
                for _, row in group.iterrows()
            }
        stop_times = pd.DataFrame(list(stop_times_dict.items()), columns=["trip_id", "route_seq"])

        # 5. Return prepared data:
        if with_stops:
            return line_routes_info, self.stops, shapes, stop_times
        else:
            return line_routes_info, shapes, stop_times

    def prepare_vehicle_data_set2(self, with_stops=False):
        """
        Prepare main data set - version 2, no pre-preparing data
        :param with_stops:
        :return:
        """
        if with_stops:
            return self.stop_times.loc[:, ["trip_id", "arrival_time", "departure_time", "stop_id", "stop_sequence"]], \
                   self.trips.loc[:, ["trip_id", "trip_headsign", "direction_id", "shape_id"]],\
                   self.stops.loc[:, ["stop_id", "stop_code", "stop_name", "stop_lat", "stop_lon", "zone_id"]],\
                   self.shapes.loc[:, ["shape_id", "shape_pt_lat", "shape_pt_lon", "shape_pt_sequence"]]
        else:
            return self.stop_times.loc[:, ["trip_id", "arrival_time", "departure_time", "stop_id", "stop_sequence"]], \
                   self.trips.loc[:, ["trip_id", "trip_headsign", "direction_id", "shape_id"]], \
                   self.shapes.loc[:, ["shape_id", "shape_pt_lat", "shape_pt_lon", "shape_pt_sequence"]]
