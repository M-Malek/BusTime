"""
Read downloaded .zip file
@M-Malek
"""
from pandas import DataFrame, read_csv
from zipfile import ZipFile, BadZipfile
from shared.tools.log_logging import main_logger


class ZIPReader:
    def __init__(self, file, load_on_start: bool = True):
        self.file = file
        self.stops = DataFrame()
        self.trips = DataFrame()
        self.stop_times = DataFrame()
        self.shapes = DataFrame()
        self.agency = DataFrame()
        self.routes = DataFrame()
        self.feed_info = DataFrame()
        self.data_list = ["stops.txt", "shapes.txt", "trips.txt", "stop_times.txt",
                          "shapes.txt", "agency.txt", "routes.txt",
                          "feed_info.txt"]  # Basic list with the names of files to import
        self.load_on_start = load_on_start
        if self.load_on_start:
            self.data_reader()

    def load_stops(self, data):
        """Load only stops file"""
        self.stops = read_csv(data, encoding="utf-8-sig", sep=',')
        # self.stops.drop(["stop_code"], axis=1) # Lepiej w read_csv określić, które kolumny importuje!!!

    def load_trips(self, data):
        """Load only trips file"""
        self.trips = read_csv(data, encoding="utf-8-sig", sep=',', usecols=["route_id", "service_id", "trip_id",
                                                                            "direction_id", "shape_id", "brigade"])
        # self.trips.drop(["brigade"], axis=1)

    def load_stop_times(self, data):
        """Load only stop_times file"""
        self.stop_times = read_csv(data, encoding="utf-8-sig", sep=',', usecols=["trip_id", "arrival_time",
                                                                                 "departure_time", "stop_id",
                                                                                 "stop_sequence", "pickup_type",
                                                                                 "drop_off_type"])
        # self.stop_times.drop(["pickup_type", "drop_off_type"], axis=1)

    def load_shapes(self, data):
        """Load only shapes file"""
        self.shapes = read_csv(data, encoding="utf-8-sig", sep=',')

    def load_agency(self, data):
        """Load only agency data"""
        self.agency = read_csv(data, encoding="utf-8-sig", sep=',', usecols=["agency_id", "agency_name", "agency_url"])

    def load_routes(self, data):
        """Load only routes data"""
        self.routes = read_csv(data, encoding="utf-8-sig", sep=',', usecols=["route_id", "agency_id", "route_long_name",
                                                                             "route_type", "route_color",
                                                                             "route_text_color"])

    def load_feed_info(self, data):
        self.feed_info = read_csv(data, encoding="utf-8-sig", sep=',')

    def data_reader(self):
        """Read data from given data list"""
        # Check variable data_list - data_list could not be give to method, then match should do default option.
        # files = self.data_list
        # Try to open and read necessary files:
        try:
            with ZipFile(self.file) as read_file:
                for entry in self.data_list:
                    match entry:
                        case "stops.txt":
                            self.load_stops(read_file.open(entry))
                        case "trips.txt":
                            self.load_trips(read_file.open(entry))
                        case "stop_times.txt":
                            self.load_stop_times(read_file.open(entry))
                        case "shapes.txt":
                            self.load_shapes(read_file.open(entry))
                        case "agency.txt":
                            self.load_agency(read_file.open(entry))
                        case "routes.txt":
                            self.load_routes(read_file.open(entry))
                        case "feed_info.txt":
                            self.load_feed_info(read_file.open(entry))
                        case _:
                            break

                read_file.close()
        except BadZipfile as e:
            # Read about most common ZipFile errors - error that file is no zip file! - most common: BadZipfile?
            main_logger("error", f"An error with opening downloaded .zip file: {e}")
