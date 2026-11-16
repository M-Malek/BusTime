class TripProgress:
    def __init__(self, trip_id, route_id, stops, current_stop_seq, detected_stops,
                 last_processed_timestamp, status, accomplished_stops_count=0,
                 last_processed_vehicle_timestamp=None, last_processed_vehicle_id=None):
        self.trip_id = trip_id
        self.route_id = route_id
        # self.vehicle_id = vehicle_id
        self.current_stop_seq = current_stop_seq
        # Current and legacy documents may contain batches; keep one flat list.
        self.detected_stops = []
        seen_observations = set()
        for item in detected_stops or []:
            batch = item if isinstance(item, list) else [item]
            for observation in batch:
                if not isinstance(observation, dict):
                    continue
                # Older Line_info documents may contain the same batch more
                # than once. Observation time plus the measured stop/location
                # identifies the repeated observation independently of delay.
                signature = (
                    observation.get("observation_time"),
                    observation.get("referenced_stop_id", observation.get("stop_id")),
                    observation.get("lat"),
                    observation.get("lng"),
                )
                if signature not in seen_observations:
                    seen_observations.add(signature)
                    self.detected_stops.append(observation)
        self.last_processed_timestamp = last_processed_timestamp
        self.last_processed_vehicle_timestamp = last_processed_vehicle_timestamp
        self.last_processed_vehicle_id = last_processed_vehicle_id
        self.status = status

        self.stops = stops
        self.all_stops_count = len(stops or [])
        self.accomplished_stops_count = accomplished_stops_count

        #self.current_stop_seq = None
        #self.detected_stops = []

        #self.last_processed_timestamp = None
        #self.status = "IN_PROGRESS"

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
            "all_stops_count": self.all_stops_count,
            "accomplished_stops_count": self.accomplished_stops_count,
            "current_stop_seq": self.current_stop_seq,
            "detected_stops": self.detected_stops,
            "last_processed_timestamp": self.last_processed_timestamp,
            "last_processed_vehicle_timestamp": self.last_processed_vehicle_timestamp,
            "last_processed_vehicle_id": self.last_processed_vehicle_id,
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
            trip_dict["status"],
            accomplished_stops_count=trip_dict.get("accomplished_stops_count", 0),
            last_processed_vehicle_timestamp=trip_dict.get("last_processed_vehicle_timestamp"),
            last_processed_vehicle_id=trip_dict.get("last_processed_vehicle_id"),
        )
