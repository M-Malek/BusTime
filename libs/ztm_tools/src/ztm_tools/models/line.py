from ztm_tools.models.route import Route


class Line:
    def __init__(self, number, agency, color, vehicle_type):
        self.line_number = number
        self.agency = agency
        self.color = color
        self.vehicle_type = vehicle_type
        self.routes = {}

    def to_dict(self) -> dict:
        return {
            "line_number": self.line_number,
            "agency": self.agency,
            "line_color": self.color,
            "vehicle_type": self.vehicle_type,
            "routes": self.routes
        }

    @classmethod
    def from_dict(cls, line_data):
        line = cls(
            number=line_data["line_number"],
            agency=line_data["agency"],
            color=line_data["line_color"],
            vehicle_type=line_data["type"],
        )

        for route_id, route_data in line_data["routes"].items():
            route = Route.from_dict(route_data)
            line.routes[route_id] = route

        return line
