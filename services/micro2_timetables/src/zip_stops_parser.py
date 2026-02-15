"""
Parse stops - find all information about Stops location in .zip file - downloaded .zip file from ZTM server
with all stop times informations
@M-Malek
"""

# Import
from services.micro2_timetables.src.zip_reader import ZIPReader
from services.micro2_timetables.src.zip_gather import zip_downloading


class Stop:
    def __init__(self, stop_id, stop_name, stop_lat, stop_lng, zone):
        self.stop_id = stop_id
        self.stop_name = stop_name
        self. stop_lat = stop_lat
        self.stop_lng = stop_lng
        self.zone = zone

    def to_dict(self) -> dict:
        return {
            "stop_id": self.stop_id,
            "name": self.stop_name,
            "lat": self.stop_lat,
            "lng": self.stop_lng,
            "zone": self.zone
        }


def zip_parser_stops(data: ZIPReader):
    """
    Parse zip file and prepare list of stops with their positions
    :param data: Ready zip file (ZIPReader object)
    :return: .json with list of stops: {"stop_code": {"name": str(stop_name), "lat": float(latitude),
    "lng": float(longitude)}}
    """
    # raw_zip = zip_downloading(url_raw_data_set)
    # raw_data_set = ZIPReader(raw_zip)
    all_unique_stops = data.stops["stop_id"].unique()

    stops_cache = {}
    stops_data = data.stops

    for stop in stops_data.itertuples(index=False):
        # stop_data = data.stops[data.stops["stop_id"] == stop_id]
        # ready_stop = Stop(int(stop_data["stop_id"]), str(stop_data["stop_name"]), float(stop_data["stop_lat"]),
        #                   float(stop_data["stop_lon"]), str(stop_data["zone_id"]))
        new_stop = Stop(int(stop.stop_id), str(stop.stop_name), float(stop.stop_lat),
                        float(stop.stop_lon), str(stop.zone_id)).to_dict()
        stops_cache[int(stop.stop_id)] = new_stop

    return stops_cache
