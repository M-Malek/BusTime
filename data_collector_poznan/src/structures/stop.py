class Stop:
    def __init__(self, data):
        # Data extracted from stop.txt - stop.txt data column heads are listened below
        # 0. stop_id, 1. stop_code, 2. stop_name, 3. stop_lat, 4. stop_lon, 5. zone_id

        # Raw data - row extracted from stops.txt file
        self.raw_data = data.split(",")
        # Stop_id - number, stop_id
        self.stop_id = int(self.raw_data[0])
        # Short name - stop codename, note: ZTM system save this variable as
        # e.g. "GORC30" - we need to remove extra " in name
        self.short_name = self.raw_data[1].replace('"', "")
        # Full name - stop full name, note: ZTM system save this variable as
        # e.g. "Miłostowo" - we need to remove extra " in name (like in self.short_name)
        self.full_name = self.raw_data[2].replace('"', "")
        # Stop latitude - need to be converted from string to float
        self.lat = float(self.raw_data[3])
        # Stop longitude - need to be converted from string to float
        self.lng = float(self.raw_data[4])
        # Stop zone - describe zone which stop belongs to:
        # A - Poznan city
        # B - cities in the immediate vicinity of the city Poznan
        # C - other cities which public transport goes to Poznan
        self.zone = self.raw_data[5]

    def identity_stop(self):
        return {
            "id": self.stop_id,
            "short_name": self.short_name,
            "full_name": self.full_name,
            "lat": self.lat,
            "lng": self.lng,
            "zone": self.zone,
        }

    def set_stop_on_map(self):
        return {
            "full_name": self.full_name,
            "lat": self.lat,
            "lng": self.lng,
            "zone": self.zone
        }

    def save_to_database(self):
        return [self.stop_id, self.full_name, self.lat, self.lng, self.zone]

