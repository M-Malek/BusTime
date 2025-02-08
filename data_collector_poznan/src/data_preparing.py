"""
data_preparing.py - data parser file
Main goal: read files with ZTM data and create pandas DataFrames with data
@created: M-Malek
"""
import zipfile
import io
import pandas
import datetime

from google.transit import gtfs_realtime_pb2
from shared.tools.filestoolbox import FilesToolBox

from data_collector_poznan.src.structures.vehicle import Vehicle as Vehicle
from data_collector_poznan.src.structures.route import Route as Route
from data_collector_poznan.src.structures.stop import Stop as Stop
from data_collector_poznan.src.structures.stop_times import RouteTimes as RouteTimes


def read_vehicle_data():
    pass


class ReadZipData(FilesToolBox):
    def __init__(self, file):
        self.file = io.BytesIO(file.content)
        self.data_date = datetime.datetime.now()
        self.routes = []
        self.stops = []
        self.times = []
        self.trips = []
        self.shapes = []
        self.list_of_files = ["routes.txt", "stops.txt", "stop_times.txt", "shapes.txt", "trips.txt"]
        # self.list_of_files = ["shapes.txt"]

    def extract_from_zip_file(self, filename):
        with zipfile.ZipFile(self.file, 'r') as zip_data:
            for file in zip_data.namelist():
                if file == filename:
                    with zip_data.open(file, 'r') as readed_file:
                        # Read content
                        content = readed_file.read()
                        # Detect file encoding
                        encoding = self.encoding_checker(content)
                        # Try to decode file with founded encoding, except UnicodeError
                        try:
                            # print(content.decode(encoding))
                            return content.decode(encoding)
                        except UnicodeError:
                            print("Wrong encoding")

    def read_data_from_zip(self):
        for file_name in self.list_of_files:
            file_content = self.extract_from_zip_file(file_name)
            file_content = file_content.split("\n")
            for row in file_content:
                if row == "" or row == '':
                    continue
                # print(row)
                if file_name == "routes.txt":
                    self.routes.append(row)
                elif file_name == "stops.txt":
                    self.stops.append(row)
                elif file_name == "stop_times.txt":
                    self.times.append(row)
                elif file_name == "shapes.txt":
                    self.shapes.append(row)
                elif file_name == "trips.txt":
                    self.trips.append(row)
