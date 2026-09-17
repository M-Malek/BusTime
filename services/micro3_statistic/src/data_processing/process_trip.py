from ztm_tools.s3_manager.download_data.file_downloader import download_data_shapes
from ztm_tools.models.trip_progress import TripProgress
from ztm_tools.models.detect_stop import DetectedStop
from ztm_tools.mongo_tools.mongo_connect import create_mongo_connection
from ztm_tools.logging.logger import main_logger
from ztm_tools.geolocation_tools.filter_points_on_route import filter_points_on_route
from ztm_tools.geolocation_tools.haversine_method import haversine
from src.mongo_service.take_mongo_data import take_mongo_data
from os import getenv

def process_trip(trip, schedules_df):
    """
    Main data processing function
    :param trip: organized data of actual Vehicle trip
    :param schedules_df: S3 data with schedules for given trip
    :return:
    """
    line_id = trip[0]
    trip = trip[1]
    # print(trip["trip_id"].unique())

    # Check if exist model TripProgress with shape_id
    # If it doesn't exist - create it
    trip_id = trip["trip_id"].unique()[0]
    route_id = trip.loc[trip["trip_id"] == trip_id, "route_id"].iloc[0]
    current_trip = take_mongo_data(trip_id, route_id)

    # In try-except: search for given by Vehicles data trip_id - if found, do calculations
    try:
        # Take one examined trip from line data
        examined_schedule = schedules_df.routes[trip_id]
        # Download shape data from S3
        shape_data = download_data_shapes(examined_schedule.shape_id)
        # The applications accept all measurements, which geolocation distance between the point and
        # next shape point is less or equal 5 meters
        filtered_points = filter_points_on_route(trip, shape_data)
        print(filtered_points)
        # We have filtered points which belong to route
        # Now, compare it with stops locations part by part to examine, if vehicle reached stop
        for point in filtered_points:
            for scheduled_point in examined_schedule:
                distance_between_points = haversine(point["lat"], point["lng"], scheduled_point["lat"], scheduled_point["lng"]) < 5
                if distance_between_points <= 5:
                    # Point in range 5 meters, to accept
                    # Calculate delay
                    delay = abs(filtered_points["timestamp"] - examined_schedule["arrival_time"])
                    print(delay)
                    # Create DetectStop object
                    # new_mes_stop = DetectedStop(
                    #
                    # )
                    # current_trip.detected_stops.append(new_mes_stop)

        # Save information's to MongoDB
        updated_trip = take_mongo_data(trip_id, route_id, current_trip)
        return updated_trip

    except KeyError:
        main_logger("error", f"Cannot identify trip_id: {trip_id} "
                            f"for line {schedules_df.line_number} ")


    """
    Example of data from MongoDB
           id       trip_id route_id        lat        lng           timestamp  seq  delay
25    425  1_2788037^N+       11  52.382690  16.929670 2026-09-10 16:21:05  NaN    NaN
621   425  1_2788037^N+       11  52.382629  16.930170 2026-09-10 16:21:33  NaN    NaN
1213  425  1_2788037^N+       11  52.381618  16.937450 2026-09-10 16:22:13  NaN    NaN
1805  425  1_2788037^N+       11  52.380409  16.942320 2026-09-10 16:22:54  NaN    NaN
2396  425  1_2788037^N+       11  52.380371  16.942490 2026-09-10 16:23:35  NaN    NaN
2985  425  1_2788037^N+       11  52.380138  16.943291 2026-09-10 16:24:05  NaN    NaN
3573  425  1_2788037^N+       11  52.380070  16.943560 2026-09-10 16:24:45  NaN    NaN
4158  425  1_2788037^N+       11  52.379929  16.944040 2026-09-10 16:25:25  NaN    NaN
4745  425  1_2788037^N+       11  52.379372  16.945730 2026-09-10 16:26:05  NaN    NaN
5329  425  1_2788037^N+       11  52.378490  16.948389 2026-09-10 16:26:33  NaN    NaN
5917  425  1_2788037^N+       11  52.376560  16.954540 2026-09-10 16:27:15  NaN    NaN
6499  425  1_2788037^N+       11  52.376068  16.955231 2026-09-10 16:27:55  NaN    NaN
7084  425  1_2788037^N+       11  52.374321  16.952971 2026-09-10 16:28:35  NaN    NaN
7671  425  1_2788037^N+       11  52.373009  16.951290 2026-09-10 16:29:05  NaN    NaN
8255  425  1_2788037^N+       11  52.372299  16.950390 2026-09-10 16:29:45  NaN    NaN
    """

