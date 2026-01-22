"""
Parse downloaded and readed .zip file
@M-Malek
"""
from services.micro2_timetables.src.zip_reader import ZIPReader
from services.micro2_timetables.src.zip_gather import zip_downloading

from pandas import merge

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


class Trip:
    def __init__(self, route_id, service_id, trip_id, shape_id):
        self.route_id = route_id
        self.service_id = service_id
        self.trip_id = trip_id
        self.shape_id = shape_id

    def to_dict(self) -> dict:
        return{
            "route_id": self.route_id,
            "service_id": self.service_id,
            "trip_id": self.trip_id,
            "shape_id": self.shape_id
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


def route_finder(data, route_id):
    routes = data.trips
    trips = routes[routes["route_id"] == route_id]

    for _, trip in trips.iterrows():
        trip = Trip(trip["trip_id"], trip["service_id"], trip["trip_id"], trip["shape_id"])
        print(trip.to_dict())


def zip_parser(url_raw_data_set):
    raw_zip = zip_downloading(url_raw_data_set)
    raw_data_set = ZIPReader(raw_zip)

    # Basic vehicle information: line number, agency, color
    # Step 1: reading all lines:
    # basic_line_info - describes basic information about the line
    basic_line_info = raw_data_set.routes[["route_id", "agency_id", 'route_color']]

    # basic_trip_info - basic information's about trips
    basic_trip_info = raw_data_set.trips[["route_id", "trip_id", "service_id", "shape_id"]]

    # Loop to finding shape set and route set
    # Find all unique sets: route_id, trip_id, shape_id
    # Debug
    # searching_set = merge(basic_line_info, basic_trip_info)[["route_id", "trip_id", "shape_id"]]
    # searching_set = basic_line_info.reset_index().merge(basic_trip_info, how="left").set_index("route_id")

    searching_set = (
        basic_line_info[["route_id"]]
        .merge(
            basic_trip_info[["route_id", "trip_id", "shape_id"]],
            on="route_id",
            how="left"
        )
        .set_index("route_id")
    )
    # Teraz z searching set należy odczytać shape_id i route_id oraz zrobić z nich zbiory danych
    # Potem zbiory danych zapisujemy z podstawowymi informacjami do bazy.
    # print(searching_set)
    # print(type(searching_set))
    all_shapes = raw_data_set.shapes
    all_times = raw_data_set.stop_times






"""
Dla każdej linii trzeba rozpisać dokładnie dane które potrzeba zapisać:
numer linii:
    id_przewoźnika: <value>,
    id_trasy:
        przebieg trasy:
            numer w sekwencji: nazwa_przystanku (id przystanku?), czas_przyjazdu, czas_odjazdu
Każda linia jako osobny .json?
Linia:
    numer,
    color,
    przewoźnik,
    trasy (trip_id): -> każda trasa ma swoje id, dzień kiedy kursuje, przebieg trasy po przystankach i shape id
    czyli przebieg trasy po mapie (do każdego z przystanków można dojechać na różne sposoby, stąd to shape!)
        id danej trasy (trip_id)
        service_id (dzień kursowania)
        shape_id
        kształt (szukany dla danego shape_id): -> potrzebny do wyświetlenia trasy pojazdu na mapie
            numer w kolejności,
            lat,
            lng,
        przebieg trasy (szukany dla danego trip_id): -> potrzebny do statystyk
            numer w kolejności (sequence),
            arrival_time,
            departure_time,
            stop_id,

Skąd jakie dane:
numer - routes.txt
color - routes.txt
przewoźnik - routes.txt
---numer, color i przewoźnik mam w basic_line_info---
trasy:
    trip_id - trips.txt
    service_id - trip.txt
    shape_id - trip.txt
    kształt trasy - shapes.txt szukamy po shape_id:
            sekwencja - shape.txt
            lat - shape.txt
            lng - shape.txt
    przebieg trasy - stop_time.txt szukamy po trip_id:
        sekwencja - stop_time.txt
        przystanek - stop_time.txt
        godzina przyjazdu (arrival time) - stop_time.txt
        godzina odjazdu (departure time) - stop_time.txt

Osobno do wczytania pozycje przystanków (do wyświetlenia na mapie, jeden wspólny plik):
stop_id
nazwa - stops.txt
lat - stops.txt
lng - stops.txt
strefa - stops.txt
"""
