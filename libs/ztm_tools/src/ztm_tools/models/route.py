from ztm_tools.models.stop_time import StopTime

class Route:
    def __init__(self, route_id, shape_id, trip_data):
        self.route_id = route_id
        self.shape_id = shape_id
        self.trip_data = trip_data

    def to_dict(self) -> dict:
        return {
            "route_id": self.route_id,
            "shape_id": self.shape_id,
            "trip_data": self.trip_data,
        }

    @classmethod
    def from_dict(cls, route_data):
        stop_times = []

        for stop_time_data in route_data["trip_data"]:
            stop_time = StopTime.from_dict(stop_time_data)
            stop_times.append(stop_time)

        return cls(
            route_id=route_data["trip_id"],
            shape_id=route_data["shape_id"],
            trip_data=stop_times,
        )
