"""
Read downloaded .zip file
@M-Malek
"""
from pandas import DataFrame, read_csv
from zipfile import ZipFile


class ZIPReader:
    def __init__(self, file):
        self.file = file
        self.stops = DataFrame()
        self.trips = DataFrame()
        self.stop_times = DataFrame()
        self.shapes = DataFrame()

    def load_stops(self, data):
        """Load only stops file"""
        self.stops = read_csv(data, encoding="utf-8-sig", sep=',')

    def load_trips(self, data):
        """Load only trips file"""
        self.trips = read_csv(data, encoding="utf-8-sig", sep=',')

    def load_stop_times(self, data):
        """Load only stop_times file"""
        self.stop_times = read_csv(data, encoding="utf-8-sig", sep=',')

    def load_shapes(self, data):
        """Load only shapes file"""
        self.shapes = read_csv(data, encoding="utf-8-sig", sep=',')

    def data_reader(self, data_list):
        """Read data from given data list"""
        # Check variable data_list - data_list could not be give to method, then match should do default option.
        try:
            with ZipFile(self.file) as readed_file:
                for entry in data_list:
                    match entry:
                        case "stops":
                            self.load_stops(readed_file.open(entry))
                        case "trips":
                            pass
                        case "stop_times":
                            pass
                        case "shapes":
                            pass
                        case _:
                            # Read all options
                            pass
                readed_file.close()
        except KeyError:
            # Read about most common ZipFile errors - error that file is no zip file!
            pass
