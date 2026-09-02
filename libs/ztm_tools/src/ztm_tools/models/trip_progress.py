class TripProgress:
    def __init__(self, trip_id, route_id, vehicle_id, stops):
        self.trip_id = trip_id
        self.route_id = route_id
        self.vehicle_id = vehicle_id

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
