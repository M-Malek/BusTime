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

    @classmethod
    def from_dict(cls, stop_dict: dict):
        return cls(
            stop_id=stop_dict["stop_id"],
            stop_name=stop_dict["stop_name"],
            stop_lat=stop_dict["stop_lat"],
            stop_lng=stop_dict["stop_lng"],
            zone=stop_dict["zone"]
        )