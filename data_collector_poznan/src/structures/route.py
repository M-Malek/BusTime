class Route:
    def __init__(self, data, shape_data):
        # Data extracted from stop.txt - route.txt data column heads are listened below
        # 0. route_id, 1. agency_id, 2.route_short_name,3. route_long_name, 4.route_desc,
        # 5. route_type, 6. route_color, 7. route_text_color
        # ZTM - Zarząd Transportu Miejskiego w Poznaniu, ang. Poznań Public Transport Authority,
        # "http://www.ztm.poznan.pl"

        # Raw data - row extracted from stops.txt file
        self.raw_data = data.split(",")
        # Route_id - ZTM's route ID number - required to right connection with route times
        self.route_id = self.raw_data[0]
        # Color - ZTM's route color
        self.color = self.raw_data[6]
        # Short route - ZTM's codename for basic route name: describes first and last vehicle stops in to pairs:
        # Górczyn - Miłostowo | Miłostowo - Górczyn
        # first pair (Górczyn - Miłostowo) = basic vehicle route (called forward in code)
        # second pair (Miłostowo - Górczyn) = vehicle way back (called backwards in code)
        self.short_route = self.raw_data[2]
        self.forward_route = self.short_route_decoder()[0]
        self.backwards_route = self.short_route_decoder()[1]
        # Long route - describe all stops on vehicle route. This data has been divided by ZTM on tree mayor parts:
        # first part - describe mayor vehicle stops and simplified vehicle route
        # second part - behind ^ delimiter - describe route enlargement
        # third part - behind | delimiter - describe if route has another course in opposite (backwards) direction
        # Long route trip data are saved using PlannedTrip class in trips.py
        self.long_route = self.raw_data[3]
        self.route_stops_id = []
        self.route_extra_stops = []

    def save_to_database(self):
        """
        Prepare data for saving in pandas.DataFrame and next, to database
        :return: list, list of basic data required for program
        """
        return [self.route_id, self.forward_route, self.backwards_route, self.route_stops_id, self.color]

    def short_route_decoder(self):
        """
        Divide short route name on two parts describing vehicle route
        :return: tuple with two elements:
                                        first element (index 0): vehicle basic route (called forward)
                                        second element (index 1): vehicle reverse route (called backward)
        """
        destination_forward = self.short_route.split("|")[0]
        destination_backwards = self.short_route.split("|")[1]
        return tuple(destination_forward, destination_backwards)

    def long_route_decoder(self, stops_ids_dict):
        """
        Translate stops names into stops_ids - NOTE: FUNCTION WITHDRAWN FROM USE
        :param stops_ids_dict: prepared dictionary of all stop names and their unique ids
        :return: none, save translation to self.route_stops_id
        """
        # Split long string with stops names into list of this names
        vehicle_route = self.long_route.split(" - ")
        routes_ids_list = []

        # Saving all names as list could require a lot of resources
        # Translate all names into stops id's - all stops have their own stop_id
        # Foreach stop name in vehicle route find and save into list named "vehicle_route_ids" stop stop_id
        for stop_name in vehicle_route:
            routes_ids_list.append(stops_ids_dict[stop_name])

        self.route_stops_id = routes_ids_list

