class TripProgress:
    def __init__(self, trip_id, route_id, stops):
        self.trip_id = trip_id
        self.route_id = route_id
        # self.vehicle_id = vehicle_id

        self.stops = stops

        self.current_stop_seq = None
        self.detected_stops = []

        self.last_processed_timestamp = None
        self.status = "IN_PROGRESS"

    def get_next_stop(self):
        if self.current_stop_seq is None:
            return self.stops[0]

        for stop in self.stops:
            if stop.seq > self.current_stop_seq:
                return stop

        return None

    def to_dict(self) -> dict:
        return {
            "trip_id": self.trip_id,
            "route_id": self.route_id,
            "stops": self.stops,
            "current_stop_seq": self.current_stop_seq,
            "detected_stops": self.detected_stops,
            "last_processed_timestamp": self.last_processed_timestamp,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, trip_dict):
        return cls(
            trip_dict["trip_id"],
            trip_dict["route_id"],
            trip_dict["stops"],
            trip_dict["current_stop_seq"],
            trip_dict["detected_stops"],
            trip_dict["last_processed_timestamp"],
            trip_dict["status"]
        )
