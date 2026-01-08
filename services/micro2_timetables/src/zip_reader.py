"""
Read downloaded .zip file
@M-Malek
"""
from pandas import DataFrame, read_csv
from zipfile import ZipFile, BadZipfile
from shared.tools.log_logging import main_logger


class ZIPReader:
    def __init__(self, file):
        self.file = file
        self.stops = DataFrame()
        self.trips = DataFrame()
        self.stop_times = DataFrame()
        self.shapes = DataFrame()
        self.data_list = ["stops", "shapes", "trips", "stop_times"] # Basic list with the names of files to import

    def load_stops(self, data):
        """Load only stops file"""
        self.stops = read_csv(data, encoding="utf-8-sig", sep=',')
        # self.stops.drop(["stop_code"], axis=1)

    def load_trips(self, data):
        """Load only trips file"""
        self.trips = read_csv(data, encoding="utf-8-sig", sep=',')
        # self.trips.drop(["brigade"], axis=1)

    def load_stop_times(self, data):
        """Load only stop_times file"""
        self.stop_times = read_csv(data, encoding="utf-8-sig", sep=',')
        # self.stop_times.drop(["pickup_type", "drop_off_type"], axis=1)

    def load_shapes(self, data):
        """Load only shapes file"""
        self.shapes = read_csv(data, encoding="utf-8-sig", sep=',')

    def data_reader(self, data_list):
        """Read data from given data list"""
        # Check variable data_list - data_list could not be give to method, then match should do default option.
        if data_list:
            files = data_list
        else:
            files = self.data_list
        # Try to open and read necessary files:
        try:
            with ZipFile(self.file) as read_file:
                for entry in files:
                    match entry:
                        case "stops":
                            self.load_stops(read_file.open(entry))
                        case "trips":
                            self.load_trips(read_file.open(entry))
                        case "stop_times":
                            self.load_stop_times(read_file.open(entry))
                        case "shapes":
                            self.load_shapes(read_file.open(entry))
                        case _:
                            break

                read_file.close()
        except BadZipfile as e:
            # Read about most common ZipFile errors - error that file is no zip file! - most common: BadZipfile?
            main_logger("error", f"An error with opening downloaded .zip file: {e}")
