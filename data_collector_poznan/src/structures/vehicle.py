class Vehicle:
    def __init__(self, number, trip_id, lat, lng, stop_sequence, delay):
        self.vehicle_number = number
        self.vehicle_trip = trip_id
        self.vehicle_route = 0
        self.lat = lat
        self.lng = lng
        self.sequence = stop_sequence
        self.delay = delay

    def identity_vehicle(self):
        return {"number": self.vehicle_number, "lat": self.lat, "lng": self.lng}

    def save_to_database(self):
        return [self.vehicle_number, self.vehicle_trip, self.lat, self.lng, self.sequence, self.delay]
