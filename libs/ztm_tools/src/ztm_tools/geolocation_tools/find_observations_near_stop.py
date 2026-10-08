from scipy.spatial import cKDTree

from ztm_tools.geolocation_tools.lat_lng_to_meters import lat_lng_to_meters
from ztm_tools.geolocation_tools.haversine_method import haversine
from ztm_tools.models.detected_observation import DetectedObservation
from ztm_tools.mongo_tools.statistic_tools.collect_stop_position import collect_stop_position


def find_observations_near_stops(filtered_points, trip_data, max_distance_m=30):
    """Zwraca obserwacje znajdujące się najwyżej max_distance_m od przystanku."""
    stop_ids = dict.fromkeys(stop["stop_id"] for stop in trip_data)

    # Pobierz współrzędne raz dla każdego unikalnego przystanku.
    stops = []
    for stop_id in stop_ids:
        lat, lng = collect_stop_position(stop_id)
        if lat is not None and lng is not None:
            stops.append({"stop_id": stop_id, "lat": lat, "lng": lng})

    if filtered_points.empty or not stops:
        return []

    stop_x, stop_y = lat_lng_to_meters(
        [stop["lat"] for stop in stops],
        [stop["lng"] for stop in stops],
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
            stop = stops[stop_index]
            distance_m = stop_tree.data[stop_index]  # współrzędne nie są odległością

            # Oblicz dokładną odległość dla dopasowanego punktu i przystanku.
            distance_m = haversine(
                point["lat"], point["lng"], stop["lat"], stop["lng"]
            )

            observations.append(
                DetectedObservation(
                    reference_stop_id=stop["stop_id"],
                    lat=point["lat"],
                    lng=point["lng"],
                    observation_time=point["timestamp"],
                    distance_to_point=distance_m,
                )
            )

    return observations
