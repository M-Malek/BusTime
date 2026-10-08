class DetectedObservation:
    def __init__(self, reference_stop_id,lat, lng, observation_time, distance_to_point):
        self.reference_stop_id = reference_stop_id
        self.lat = lat
        self.lng = lng
        self.observation_time = observation_time
        self.distance_to_point = distance_to_point

    def to_dict(self):
        return {"referenced_stop_id": self.reference_stop_id,"lat": self.lat,
                "lng": self.lng, "observation_time": self.observation_time,
                "distance_to_point": self.distance_to_point}

    @classmethod
    def from_dict(cls, data):
        return cls(
            lat=data["lat"],
            lng=data["lng"],
            observation_time=data["observation_time"],
            distance_to_point=data["distance_to_point"],
        )
