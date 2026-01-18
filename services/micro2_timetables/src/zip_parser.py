"""
Parse downloaded and readed .zip file
@M-Malek
"""
from services.micro2_timetables.src.zip_reader import ZIPReader
from services.micro2_timetables.src.zip_gather import zip_downloading


class Stop:
    def __init__(self, stop_id, arv_time, dep_time, seq):
        self.stop_id = stop_id
        self.arv_time = arv_time
        self.dep_time = dep_time
        self.seq = seq

    def load(self):
        """Load Stop information"""
        pass

    def to_dict(self) -> dict:
        return {
            "stop_id": self.stop_id,
            "arv_time": self.arv_time,
            "dep_time": self.dep_time,
            "seq": self.seq
        }


class Routes:
    def __init__(self, route_id):
        self.route_id = route_id
        self.stops = {}

    def load(self):
        pass

    def to_dict(self) -> dict:
        return {
            "route_id": self.route_id,
            "stops": self.stops,
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


class ZIPParser:
    def __init__(self, url_raw_data_set):
        self.raw_zip = zip_downloading(url_raw_data_set)
        self.raw_data_set = ZIPReader(self.raw_data_set)
        # Main task: prepare data:
        # Idea: store data by line numbers (trip_id etc.)

    def vehicle_line_parser(self):
        pass

    def stops_parser(self):
        pass

    def vehicles_parser(self):
        # vehicle = Vehicle('222')
        pass


def zip_parser(url_raw_data_set):
    raw_zip = zip_downloading(url_raw_data_set)
    raw_data_set = ZIPReader(raw_zip)

    # Basic vehicle information: line number, agency, color
    # Step 1: reading all lines:
    basic_line_info = raw_data_set.routes[["route_id", "agency_id", 'route_color']]
    # Debug:
    print(basic_line_info.head(10))

"""
Dla każdej linii trzeba rozpisać dokładnie dane które potrzeba zapisać:
numer linii:
    id_przewoźnika: <value>,
    id_trasy:
        przebieg trasy:
            numer w sekwencji: nazwa_przystanku (id przystanku?), czas_przyjazdu, czas_odjazdu
Każda linia jako osobny .json?
"""
