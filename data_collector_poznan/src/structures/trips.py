class PlannedTrip:
    """
    According to ZTM documentation, PlannedTrip has to describe whole vehicle route
    Depending on trip ID, vehicle route have different stops
    PlannedTrip class has to describe this route based on information from files:
    shapes.txt
    route.txt
    stop_times.txt
    trip.txt

    Data required to save:
    basic trip data:
    trip id - PRIMARY KEY?,
    route id,
    trip type: basic, with changes - how to describe it?
    trip changes description,

    route in format:
    trip_id - PRIMARY KEY,
    route id,
    sequence number,
    stop_id,
    stop arrival time,
    stop departure time,

    This data could be saved:
    - as json file,
    - in MongoDB database
    - in two separate Postgres tables: table one: basic trip data, table two: route data
    """
    def __init__(self, shapes, routes, trip, stop_times):
        # Source files
        self.shapes_data = shapes
        self.routes_data = routes
        self.trip_data = trip
        self.stop_times_data = stop_times

        # Data to save in database
        self.trip_id = 0
        self.route_id = 0
        self.route_name = ""
        self.seqence_number = 0
        self.stop_id = 0
        self.arrival_time = 0
        self.departure_time = 0

    def set_parameters(self):
        pass


class ActualTrip:
    """
    ActualTrip has to describe actual vehicle trip
    Need to save:
    route_id,
    trip_id,
    lat,
    lng,
    delay,
    """
    def __init__(self):
        self.route_id = 0
        self.trip_id = 0
        self.actual_lat = 0
        self.actual_lng = 0
        self.delay = 0

    def set_parameters(self):
        pass

