from ztm_tools.s3_manager.download_data.file_downloader import download_data_shapes
from ztm_tools.logging.logger import main_logger
from ztm_tools.geolocation_tools.filter_points_on_route import filter_points_on_route
from src.mongo_service.take_mongo_data import take_mongo_data
from ztm_tools.geolocation_tools.find_observations_near_stop import find_observations_near_stops
from ztm_tools.mongo_tools.statistic_tools.collect_stop_position import collect_stop_position

def process_trip(trip, schedules_df):
    """
    Main data processing function
    :param trip: organized data of actual Vehicle trip
    :param schedules_df: S3 data with schedules for given trip
    :return:
    """
    line_id = trip[0]
    trip = trip[1]

    # Check if exist model TripProgress with shape_id
    # If it doesn't exist - create it
    trip_id = trip["trip_id"].unique()[0]
    route_id = trip.loc[trip["trip_id"] == trip_id, "route_id"].iloc[0]
    current_trip = take_mongo_data(trip_id, route_id)

    # Step 1: load all necessary data:
    # Prepare reference trip data from .zip files - it is theoretical vehicle route
    try:
        examined_schedule = schedules_df.routes[trip_id]
    except KeyError as e:
        main_logger("error", f"Cannot identify trip_id: {trip_id}")
        return None

    # Load stops data - schedules_df contains only stop_id for our route - we need to load stops locations first
    stops = {}
    for scheduled_point in examined_schedule["trip_data"]:
        stops[scheduled_point["stop_id"]] = collect_stop_position([scheduled_point["stop_id"]])

    # Try to find shape data - if it doesn't exist we cannot check if points are on vehicle road - this data
    # cannot be accepted - return None and skip this route
    # print("Debug: ", examined_schedule["shape_id"])
    try:
        shape_data = download_data_shapes(examined_schedule["shape_id"])
    except Exception as e:
        main_logger("error", f"Error while downloading shapes: {e}")
        main_logger("info", f"There is no shape data for trip_id: {trip_id}")
        return None

    # Step 2: finding measurement points:
    # Find all points belongs to vehicle route - if there was an error or there were no points, return None
    try:
        filtered_points = filter_points_on_route(trip, shape_data)
    except Exception as e:
        main_logger("error", f"Error while filtering points on route: trip_id: {line_id}")
        return None

    if len(filtered_points.index) == 0:
        main_logger("error", f"There was no points which belongs to trip_id: {trip_id}")
        return None

    # Step 3: calculations
    # Calculate, which points from filtered_points are close to stop, add them as observations of detected stops
    observation_points = find_observations_near_stops(filtered_points, examined_schedule["trip_data"])

    # Step 4:
    # Add information to current_trip
    # Prepare list of stops_id to save as list:
    stop_id_list = list(stops.keys())

    # Add stops to trip information, if stops is empty
    # print(current_trip)
    if current_trip.stops is None:
        current_trip.stops = stop_id_list
    elif len(current_trip.stops) == 0:
        current_trip.stops = stop_id_list
    current_trip.detected_stops.append(observation_points)
    saved_data = take_mongo_data(trip_id, route_id, current_trip)
    main_logger("info", f"Saved data for trip: {saved_data.trip_id}")
    return current_trip
