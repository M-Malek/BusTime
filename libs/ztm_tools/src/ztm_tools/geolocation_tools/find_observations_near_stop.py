from scipy.spatial import cKDTree

from ztm_tools.geolocation_tools.lat_lng_to_meters import lat_lng_to_meters
from ztm_tools.geolocation_tools.haversine_method import haversine
from ztm_tools.models.detected_observation import DetectedObservation


def find_observations_near_stops(filtered_points, trip_data, stops, max_distance_m=30):
    """Zwraca obserwacje znajdujące się najwyżej max_distance_m od przystanku."""
    if filtered_points.empty or not stops:
        return []

    # `stops` ma postać {stop_id: (lat, lng)}. Zachowujemy tę samą
    # kolejność dla współrzędnych drzewa i identyfikatorów przystanków.
    stop_ids = list(stops)
    stop_positions = [stops[stop_id] for stop_id in stop_ids]
    stop_x, stop_y = lat_lng_to_meters(
        [position[0] for position in stop_positions],
        [position[1] for position in stop_positions],
    )

    stop_tree = cKDTree(list(zip(stop_x, stop_y)))

    point_x, point_y = lat_lng_to_meters(
        filtered_points["lat"].to_numpy(),
        filtered_points["lng"].to_numpy(),
    )
    point_coordinates = list(zip(point_x, point_y))

    observations = []
    for point_index, nearby_stop_indices in enumerate(
        stop_tree.query_ball_point(point_coordinates, r=max_distance_m)
    ):
        point = filtered_points.iloc[point_index]

        for stop_index in nearby_stop_indices:
            stop_id = stop_ids[stop_index]
            stop_lat, stop_lng = stop_positions[stop_index]

            # Oblicz dokładną odległość dla dopasowanego punktu i przystanku.
            distance_m = haversine(
                point["lat"], point["lng"], stop_lat, stop_lng
            )
            if distance_m > max_distance_m:
                continue

            observations.append(
                DetectedObservation(
                    reference_stop_id=stop_id,
                    lat=point["lat"],
                    lng=point["lng"],
                    observation_time=point["timestamp"],
                    distance_to_point=distance_m,
                    sequence=point["seq"],
                ).to_dict()
            )

    return observations
