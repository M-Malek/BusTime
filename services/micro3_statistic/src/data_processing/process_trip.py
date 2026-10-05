from ztm_tools.s3_manager.download_data.file_downloader import download_data_shapes
from ztm_tools.models.trip_progress import TripProgress
from ztm_tools.models.detect_stop import DetectedStop
from ztm_tools.mongo_tools.mongo_connect import create_mongo_connection
from ztm_tools.logging.logger import main_logger
from ztm_tools.geolocation_tools.filter_points_on_route import filter_points_on_route
from ztm_tools.geolocation_tools.haversine_method import haversine
from src.mongo_service.take_mongo_data import take_mongo_data
from os import getenv
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
    # print("Current trip_id: ", trip_id)
    # print("Current route_id: ", route_id)
    # a = input("wait")
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
    try:
        shape_data = download_data_shapes(examined_schedule["shape_id"])
    except Exception as e:
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
    # First, let's check if we have sequence data - it's easiest way to check data
    # print("----------------Filtered points-----------")
    # print(filtered_points)
    # print("---------------------------")
    # print(type(filtered_points))
    if filtered_points["seq"].isna().any():
        # Filtered_points has None or NaN - we need to compare all points with reference points
        pass
    else:
        # Filtered_points has sequence data - we need to check some first and last points and calculate
        pass

    # d = input()
    # In try-except: search for given by Vehicles data trip_id - if found, find all points for given route
    # try:
    #     # Take one examined trip from line data
    #     examined_schedule = schedules_df.routes[trip_id]
    #     # Download shape data from S3
    #     shape_data = download_data_shapes(examined_schedule["shape_id"])
    #     # The applications accept all measurements, which geolocation distance between the point and
    #     # next shape point is less or equal 5 meters
    #
    #     # Find positions of all stops on Vehicle route
    #     try:
    #         filtered_points = filter_points_on_route(trip, shape_data)
    #     except Exception as e:
    #         main_logger("error", f"Error while filtering points on route: line: {line_id}")
    #
    #     # We have filtered points which belong to route
    #     # Now, compare it with stops locations part by part to examine, if vehicle reached stop
    #     # only for debug:
    #     updated_trip = []
    #
    #     # If len(filtered_points.index) > 0 -> that's mean that we have some points which belongs to route
    #     if len(filtered_points.index) != 0:
    #         # Download data of stops:
    #         stops = {}
    #         for scheduled_point in examined_schedule["trip_data"]:
    #             stops[scheduled_point["stop_id"]] = collect_stop_position([scheduled_point["stop_id"]])
    #
    #
    #
    #         for _, point in filtered_points.iterrows():
    #             for scheduled_point in examined_schedule["trip_data"]:
    #                 # print(scheduled_point)
    #                 # c = input("wait...")
    #                 # scheduled_point is now a dictionary with information about trip with parameters:
    #                 # {'seq', 'stop_id', 'arv_time', 'dep_time', 'pickup', 'dropoff'}
    #                 # Now it's necessary to find stop_id coordinates
    #                 # stop_lat, stop_lng = collect_stop_position(scheduled_point["stop_id"])
    #                 stop_lat = stops[scheduled_point["stop_id"]][0]
    #                 stop_lng = stops[scheduled_point["stop_id"]][1]
    #                 if stop_lat is not None and stop_lng is not None:
    #                     print(point["lat"], point["lng"], stop_lat, stop_lng)
    #                     distance_between_points = haversine(point["lat"], point["lng"], stop_lat, stop_lng)
    #                     print("Distance between points: ", distance_between_points)
    #                     b = input('wait...')
    #                     # ERROR HERE!
    #                     # Distance between points is huge: 52.39297866821289 16.88636016845703 52.38342 16.8345 -> more
    #                     # than 3 kilometers! Check:
    #                     # 1. If examined_schedule and shape_data are data for the same schedule
    #                     # 2. Check if rounding data by MongDB does not destroy them
    #                     # 3. Check idea!
    #                 #     if distance_between_points <= 5:
    #                 #         print(f"For point {point['lat']}, {point['lng']}, we have stop {scheduled_point['stop_id']}({stop_lat}, {stop_lng})"
    #                 #               f"in range of 5 meters! Adding to delay calculations!")
    #                 #         # Point in range 5 meters, to accept
    #                 #         # Calculate delay
    #                 #         delay = abs(filtered_points["timestamp"] - examined_schedule["arrival_time"])
    #                 #         print(delay)
    #                 #         updated_trip.append([
    #                 #             point,
    #                 #             delay
    #                 #         ])
    #                         # Create DetectStop object
    #                         # new_mes_stop = DetectedStop(
    #                         #
    #                         # )
    #                         # current_trip.detected_stops.append(new_mes_stop)
    #
    #     # Save information's to MongoDB
    #     # updated_trip = take_mongo_data(trip_id, route_id, current_trip)
    #     return updated_trip
    #
    # except KeyError as e:
    #     main_logger("error", f"Cannot identify trip_id: {trip_id} "
    #                         f"for line {schedules_df['line_number'].unique()[0]}. Error: {e} ")


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

"""
Gather data:
        id      trip_id route_id        lat        lng           timestamp  seq  delay
323    188  1_2787338^S        1  52.393410  16.886360 2026-09-10 16:21:05  NaN    NaN
919    188  1_2787338^S        1  52.392979  16.886360 2026-09-10 16:21:35  NaN    NaN
1512   188  1_2787338^S        1  52.392639  16.887260 2026-09-10 16:22:15  NaN    NaN
2105   188  1_2787338^S        1  52.391109  16.891470 2026-09-10 16:22:54  NaN    NaN
2697   188  1_2787338^S        1  52.390320  16.893669 2026-09-10 16:23:35  NaN    NaN
3288   188  1_2787338^S        1  52.390049  16.894409 2026-09-10 16:23:55  NaN    NaN
3873   188  1_2787338^S        1  52.389690  16.895420 2026-09-10 16:24:36  NaN    NaN
4463   188  1_2787338^S        1  52.388630  16.898399 2026-09-10 16:25:25  NaN    NaN
5047   188  1_2787338^S        1  52.387070  16.902960 2026-09-10 16:26:05  NaN    NaN
5631   188  1_2787338^S        1  52.386921  16.903391 2026-09-10 16:26:33  NaN    NaN
6215   188  1_2787338^S        1  52.386089  16.908270 2026-09-10 16:27:14  NaN    NaN
6796   188  1_2787338^S        1  52.385330  16.913960 2026-09-10 16:27:55  NaN    NaN
7382   188  1_2787338^S        1  52.385269  16.914070 2026-09-10 16:28:35  NaN    NaN
7966   188  1_2787338^S        1  52.384960  16.914650 2026-09-10 16:28:56  NaN    NaN
8551   188  1_2787338^S        1  52.383980  16.918350 2026-09-10 16:29:45  NaN    NaN
9141   188  1_2787338^S        1  52.383221  16.924980 2026-09-10 16:30:25  NaN    NaN
9729   188  1_2787338^S        1  52.382702  16.929630 2026-09-10 16:31:05  NaN    NaN
10316  188  1_2787338^S        1  52.382252  16.933340 2026-09-10 16:31:34  NaN    NaN
10901  188  1_2787338^S        1  52.380741  16.941231 2026-09-10 16:32:15  NaN    NaN
11480  188  1_2787338^S        1  52.380421  16.942329 2026-09-10 16:32:55  NaN    NaN
12064  188  1_2787338^S        1  52.380009  16.943010 2026-09-10 16:33:16  NaN    NaN
12648  188  1_2787338^S        1  52.379318  16.942751 2026-09-10 16:34:05  NaN    NaN
13230  188  1_2787338^S        1  52.377991  16.941891 2026-09-10 16:34:45  NaN    NaN
13813  188  1_2787338^S        1  52.376541  16.940350 2026-09-10 16:35:25  NaN    NaN
14400  188  1_2787338^S        1  52.375759  16.939489 2026-09-10 16:35:55  NaN    NaN
14984  188  1_2787338^S        1  52.371620  16.935089 2026-09-10 16:36:35  NaN    NaN
15566  188  1_2787338^S        1  52.370861  16.934259 2026-09-10 16:37:15  NaN    NaN
16150  188  1_2787338^S        1  52.368408  16.931690 2026-09-10 16:37:55  NaN    NaN
Reference data:
     sequence   latitude  longitude
0           0  52.383429  16.834338
1           1  52.383690  16.835223
2           2  52.383952  16.835946
3           3  52.384997  16.838588
4           4  52.385078  16.838795
..        ...        ...        ...
148       148  52.369485  16.932948
149       149  52.369277  16.932726
150       150  52.369061  16.932520
151       151  52.368718  16.932210
152       152  52.368340  16.931826

[153 rows x 3 columns]

52.39297866821289 16.88636016845703 52.38342 16.8345
Distance between points:  3676.3915682007305
wait...
52.39297866821289 16.88636016845703 52.38506531 16.8391843
Distance between points:  3320.168646006671
wait...
52.39297866821289 16.88636016845703 52.386637 16.844399
Distance between points:  2933.529245439627
wait...
52.39297866821289 16.88636016845703 52.38845674 16.84981792
Distance between points:  2530.196515757401
wait...
52.39297866821289 16.88636016845703 52.389826 16.853427
Distance between points:  2262.1159966785895
wait...
52.39297866821289 16.88636016845703 52.392 16.85783
Distance between points:  1939.0161935317221
wait...
52.39297866821289 16.88636016845703 52.39535426 16.8623584
Distance between points:  1649.899543334821
wait...
52.39297866821289 16.88636016845703 52.39659002 16.86686669
Distance between points:  1382.3055029998363
wait...
52.39297866821289 16.88636016845703 52.39889837 16.87600714
Distance between points:  962.6733252642115
wait...
52.39297866821289 16.88636016845703 52.40033631 16.88154192
Distance between points:  881.031642272721
"""