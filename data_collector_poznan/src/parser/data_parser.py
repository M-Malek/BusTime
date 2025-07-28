"""
data_parser.py - data parser file
Main goal: read files with ZTM data and prepare it to saving on
@created: M-Malek
"""
import zipfile
import io
import pandas
import datetime

from google.transit import gtfs_realtime_pb2
from shared.tools.filestoolbox import FilesToolBox


class BasicZipData(FilesToolBox):
    def __init__(self, file, names):
        self.file = io.BytesIO(file.content)
        self.data_date = datetime.datetime.now()
        self._files_names = names
        self.basic_files_dict = {}
        self.routes = pandas.DataFrame
        self.stops = pandas.DataFrame
        self.prepare_routes()

    @property
    def files_names(self):
        return self._files_names

    @files_names.setter
    def file_names(self, names):
        if isinstance(names, tuple):
            for name in tuple:
                if not isinstance(name, str):
                    raise ValueError("File name must be a string!")
                if name not in ["routes.txt", "stops.txt"]:
                    raise TypeError("The BasicZipData class can only be used to read routes.txt and stops.txt files. "
                                    "In other cases, use the PrepareZip class ")
        else:
            raise ValueError("File names has to be a tuple with data")
        self._files_names = names

    def prepare_data(self, file_to_save):
        with zipfile.ZipFile(self.file, 'r') as zip_data:
            for file_name in zip_data.namelist():
                if file_name in self.files_names:
                    with zip_data.open(file_name) as examined_file:
                        file_encoding = self.encoding_checker(examined_file.read())
                        for row in examined_file:
                            print(row.strip())
                        if file_to_save == "stops.txt":
                            # self.stops = pandas.read_csv(examined_file, engine="pyarrow", encoding=file_encoding,
                            #                              on_bad_lines=self.log_bad_line)
                            # self.stops = pandas.read_csv(examined_file, delimiter=',')
                            pass
                        elif file_to_save == "routes.txt":
                            # self.routes = pandas.read_csv(examined_file, engine="pyarrow", encoding=file_encoding,
                            #                               on_bad_lines=self.log_bad_line)
                            # self.routes = pandas.read_csv(examined_file, delimiter=',')
                            pass

    def prepare_stops(self):
        self.files_names = "stops.txt"
        self.prepare_data("stops.txt")
        self.files_names = "routes.txt"

    def prepare_routes(self):
        self.prepare_data("routes.txt")


class PrepareZip(FilesToolBox):
    def __init__(self, file):
        # Declaration of file with data
        self.file = io.BytesIO(file.content)
        self.data_date = datetime.datetime.now()

        # Declaration of all possible data
        self.agency = pandas.DataFrame()
        self.calendar = pandas.DataFrame()
        self.calendar_dates = pandas.DataFrame()
        self.feed_info = pandas.DataFrame()
        self.routes = pandas.DataFrame()
        self.shapes = pandas.DataFrame()
        self.stops = pandas.DataFrame()
        self.stop_times = pandas.DataFrame()
        self.trips = pandas.DataFrame()

    def read_all_zip(self):
        with zipfile.ZipFile(self.file, 'r') as zip_data:
            for file_name in zip_data.namelist():
                # print(file_name.title().lower())
                with zip_data.open(file_name) as raw_file:
                    file_encoding = self.encoding_checker(raw_file)
                    self.prepare_all_data(raw_file.name, raw_file, file_encoding)
                    raw_file.close()
            zip_data.close()

    def prepare_all_data(self, file_name, file_content, file_encoding):
        # Function to re-work: Read all file names in .zip then load one by one and save results as pandas.DataFrame
        # with name of .txt file
        if file_name == "agency.txt":
            # raw_data = file_content.read().decode('utf-8')
            # self.agency = pandas.read_csv(raw_data, sep=',')
            self.agency = pandas.read_csv(file_content, sep=',', encoding=file_encoding)

        if file_name == "calendar.txt":
            self.calendar = pandas.read_csv(file_content, sep=',', encoding=file_encoding)

        if file_name == "calendar_dates.txt":
            self.calendar_dates = pandas.read_csv(file_content, sep=',', encoding=file_encoding)

        if file_name == "feed_info.txt":
            self.feed_info = pandas.read_csv(file_content, sep=',', encoding=file_encoding)
            # self.feed_info.insert(5, "download_date", datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
            # print(self.feed_info)

        if file_name == "routes.txt":
            self.routes = pandas.read_csv(file_content, sep=',', encoding=file_encoding)

        if file_name == "shapes.txt":
            self.shapes = pandas.read_csv(file_content, sep=',', encoding=file_encoding)

        if file_name == "stops.txt":
            self.stops = pandas.read_csv(file_content, sep=',', encoding=file_encoding)

        if file_name == "stop_times.txt":
            self.stop_times = pandas.read_csv(file_content, sep=',', encoding=file_encoding)

        if file_name == "trips.txt":
            self.trips = pandas.read_csv(file_content, sep=',', encoding=file_encoding)

#     Mój diagram - zmiany na klasy, uporządkować w nowym diagramie. Trzeba dodać że read_file odczytuje .zip, potem
#     plik feed_info potem porównuje z tym co już jest w bazie i dopiero potem zapisuje zmiany (jeżeli są konieczne)


def prepare_feeds(data):
    prepared_data = {}
    for entry in data.entity:
        if entry.HasField('entity'):
            timestamp = entry.timestamp
            trip_id = entry.emtity.vehicle.trip.trip_id
            vehicle_id = entry.vehicle.vehicle.id
            lat = entry.vehicle.position.latitiude
            lng = entry.vehicle.position.longitude
            current_stop = entry.vehicle.current_stop_sequence
        # Add data to prepared data - one entry = all data from one loop
    print(data)
