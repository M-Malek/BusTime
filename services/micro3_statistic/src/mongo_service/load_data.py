

def load_data():
    """
    Load data from MongoDB and S3
    :return: shapes, schedule,
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