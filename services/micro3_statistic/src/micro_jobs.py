"""
Micro3 jobs
@M-Malek
"""

from src.mongo_service.vehicle_location_importer import vehicles_data_downloader
from src.mongo_service.vehicles_data_organizer import organize_vehicles_data
from src.s3_service.s3_data_downloader import download_s3_data
#  Remember: after downloading data from ZTM Micro 3 has to give info to Micro 2 - replace data!
def job_statistic():
    """
    Main microservice 3 job: statistic
    :return:
    """
    """
    TODO:
    1. Import data from mongo
    2. Organize data by route_id
    3. For each set of organized data: - its data of single route
    4. Group data by trip_id
    5. Load file with schedules from S3
    6. Find trip_id in S3 data
    7. Pair timestamp of entry from Mongo with timestamp of S3 data
    8. Calculate delay and add to list of delays
    9. Next create: median and mean of entries
    10. Find biggest delay
    11. Save data in Mongo for given vehicle
    12. Send message to SQS form Microservice 2?
    """
    # 1. Import data from mongo - vehicles_pos
    vehicles_pos = vehicles_data_downloader()
    # 2. Organize data by route_id
    organized_vehicles = organize_vehicles_data(vehicles_pos)
    # 3. For schedule with given route_id (route_id is the number of ZTM line, e.g. 1, 7, 11, 190, 167
    for route_id, route_df in organized_vehicles:
        # Group data by trip_id (trip_id is an id describing route of vehicle with stop times)
        organized_vehicles_trips = route_df.groupby("trip_id")
        line_number = route_id[0]
        # Load data from S3 for examined route_id:
        schedules_df = download_s3_data(line_number)
        # schedules_df has all information from .json file. Now it's simple: compare data from Mongo and .json files
        for trip in organized_vehicles_trips:
            if trip in schedules_df.routes.items():
                print("Znaleziono trasę: ", trip)
                print(schedules_df.routes[trip])
            a = input("await")