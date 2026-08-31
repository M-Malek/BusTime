class Shape:
    def __init__(self, seq, lat, lon):
        self.sequence = seq
        self.latitude = lat
        self.longitude = lon

    def to_dict(self) -> dict:
        return {
            "sequence": self.sequence,
            "latitude": self.latitude,
            "longitude": self.longitude
        }
