"""
Parse stops - find all information about Stops location in .zip file - downloaded .zip file from ZTM server
with all stop times informations
@M-Malek
"""

# Import
from services.micro2_timetables.src.zip_reader import ZIPReader
from services.micro2_timetables.src.zip_gather import zip_downloading


class Stop:
    def __init__(self, stop_id, stop_name, stop_lat, stop_lng):
        self.stop_id = stop_id
        self.stop_name = stop_name
        self. stop_lat = stop_lat
        self.stop_lng = stop_lng

    def to_dict(self) -> dict:
        return {
            "stop_id": self.stop_id,
            "name": self.stop_name,
            "lat": self.stop_lat,
            "lng": self.stop_lng
        }


def zip_parser_stops(url_raw_data_set):
    """
    Parse zip file and prepare list of stops with their positions
    :param url_raw_data_set: url to .zip file with GTFS file
    :return: .json with list of stops: {"stop_code": {"name": str(stop_name), "lat": float(latitude),
    "lng": float(longitude)}}
    """
    raw_zip = zip_downloading(url_raw_data_set)
    raw_data_set = ZIPReader(raw_zip)
    all_unique_stops = raw_data_set.stops["stop_id"].unique()

    stops_cache = {}

    for stop_id in all_unique_stops:
        pass
#        Work in progress...
