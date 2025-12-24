"""
Manage downloaded feeds file
@M-Malek
"""

import datetime

import pandas

from data_collector_poznan.src.gather.feeds_gater import download_vehicle_data


def feeds_manager(url_vehicle, url_feeds):
    """
    Returns prepared data downloaded from feeds file
    :param url_vehicle: URL for ZTM's vehicle_positions.pb
    :param url_feeds: URL for ZTM's feeds.pb
    :return: dict with data to save to file
    """

    # Raw data:
    # Debug: time measurements:
    time1 = datetime.datetime.now()
    data_vehicle = download_vehicle_data(url_vehicle)
    data_feeds = download_vehicle_data(url_feeds)

    # Error check: if data download failed - data_vehicle and data_feeds == None, return error log and exit
    if data_vehicle is None or data_feeds is None:
        print(f"{datetime.datetime.now()} - Error during data download! Data skipped!")
        return None
    # Debug: time measurements:
    time2 = datetime.datetime.now()
    # "Storages" for raw data:
    data_vehicle_raw = []
    data_feeds_raw = []

    # 1. Take data from data_vehicle: id, trip_id, route_id, lat, lng, timestamp
    # Save data as new dict in data_vehicle_raw

    # Debug: time measurements:
    time3 = datetime.datetime.now()
    for entity in data_vehicle.entity:
        if not entity.HasField("vehicle"):
            continue

        vehicle_id = entity.id
        trip_id = entity.vehicle.trip.trip_id
        route_id = entity.vehicle.trip.route_id
        lat = entity.vehicle.position.latitude
        lng = entity.vehicle.position.longitude
        timestamp = entity.vehicle.timestamp
        ready_set = {
            "id": vehicle_id,
            "trip_id": trip_id,
            "route_id": route_id,
            "lat": lat,
            "lng": lng,
            "timestamp": datetime.datetime.fromtimestamp(timestamp),
        }
        data_vehicle_raw.append(ready_set)

    # Debug: time measurements:
    time4 = datetime.datetime.now()

    # 2. Take data from feeds_pb: id, trip_id, seq, delay, timestamp
    # Save data as new dict in data_feeds_raw

    # Debug: time measurements:
    time5 = datetime.datetime.now()
    # print(data_feeds)
    for entity in data_feeds.entity:
        if not entity.HasField("trip_update"):
            continue

        trip_update = entity.trip_update
        stop_time_updates = trip_update.stop_time_update

        if len(stop_time_updates) == 0:
            continue

        first_stu = stop_time_updates[0]

        data_feeds_raw.append({
            "id": entity.id,
            "trip_id": trip_update.trip.route_id,
            "seq": first_stu.stop_sequence,
            "delay": first_stu.arrival.delay if first_stu.HasField("arrival") else None,
            "timestamp": datetime.datetime.fromtimestamp(trip_update.timestamp),
        })

    # Debug: time measurements:
    time6 = datetime.datetime.now()
    # print(data_feeds_raw[2])

    # 3. Using route_id and id connect both list: save results as result list of dicts ready to save in db
    # Recreate both list with data as maps:
    # For vehicle
    vehicle_map = {}
    for entry in data_vehicle_raw:
        trip_id = entry["trip_id"]
        vehicle_map[trip_id] = entry

    # For feed:
    feed_map = {}
    for entry in data_feeds_raw:
        trip_id = entry["trip_id"]
        feed_map[trip_id] = entry

    # Find all unique "trip_id" in both maps
    all_trip_ids = set(vehicle_map.keys()) | set(feed_map.keys())

    # Place to store ready data:
    combined_data = []

    # Iterate true unique set and read all required data. No given data = None
    for trip_id in all_trip_ids:
        # Take data from map for vehicle or feed
        vehicle = vehicle_map.get(trip_id)
        feed = feed_map.get(trip_id)

        # Debug:
        # print(feed) - feed is None!
        # Select required data and save as ready set
        combined_entry = {
            "id": vehicle["id"] if vehicle else None,
            "trip_id": trip_id,
            "route_id": vehicle["route_id"] if vehicle else (feed["trip_id"] if feed else None),
            "lat": vehicle["lat"] if vehicle else None,
            "lng": vehicle["lng"] if vehicle else None,
            "timestamp": vehicle["timestamp"] if vehicle else (feed["timestamp"] if feed else None),
            # "seq": feed["seq"] if feed else None,
            # Only for debug
            "seq": feed["seq"] if feed else "No feed file",
            # "delay": feed["delay"] if feed else None,
            # Only for debug
            "delay": feed["delay"] if feed else "No feed file",
        }
        combined_data.append(combined_entry)

    # Debug: time measurements
    time7 = datetime.datetime.now()
    print(f"Length data_vehicle: {len(data_vehicle_raw)}, length data_feed: {len(data_feeds_raw)}")
    # print(f"Debug: time:"
    #       f"Start time: {time1}\n"
    #       f"Data downloaded: {time2-time1}\n"
    #       f"Start of reading vehicle data: {time3}\n"
    #       f"Vehicle data read in {time4-time3}\n"
    #       f"Start of reading feeds data: {time5}\n"
    #       f"Feeds data read in {time6-time5}\n"
    #       f"All data has been prepared in {time7-time1} seconds")
    # Statistic for 100 runs: avg. seconds to prepare data (tested by data_collector_tests - test 1.

    return pandas.DataFrame(combined_data)

