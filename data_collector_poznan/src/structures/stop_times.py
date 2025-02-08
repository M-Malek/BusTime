class RouteTimes:
    def __init__(self, data):
        # 0. trip_id, 1. arrival_time, 2. departure_time, 3. stop_id, 4. stop_sequence,
        # 5. stop_headsign, 6. pickup_type, 7. drop_off_type
        self.raw_data = data.split(',')
        self.trip_id = self.raw_data[0]
        self.arrival_time = self.raw_data[1]
        self.departure_time = self.raw_data[2]
        self.stop_id = self.raw_data[3]
        self.stop_sequence = self.raw_data[4]
    
    def save_to_database(self):
        return [self.trip_id, self.arrival_time, self.departure_time, self.stop_id, self.stop_sequence]
