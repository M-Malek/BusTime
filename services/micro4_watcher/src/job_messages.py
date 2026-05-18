import boto3
import json
import os
from src.sqs_messages import message_creator


# def message_vehicles_wipeout():
#    message_creator(MESSAGES_SET["vehicle_wipeout"][0], MESSAGES_SET["vehicle_wipeout"][1])
MESSAGES_SET = {
    # "vehicle_update": ("GTFS_UPDATED", ["feeds.pb", "vehicles.pb"]),
    # "vehicle_wipeout": ("GTFS_WIPEOUT", ["MONGO_DB"]),
    "stoptimes_normal": ("STOP_TIMES_NORMAL", "microservice_2", "vehicle_data", "update", f"S3/ztm_poznan"),
    "stoptimes_shapes": ("STOP_TIMES_SHAPES", "microservice_2", "shape_data", "download/shape", ""),
    "stoptimes_stops": ("STOP_TIMES_STOPS", "microservice_2", "stops_data", "download/stops", "MONGODB/stops"),
    "statistic_normal": ("STATISTIC_NORMAL", "microservice_3", "vehicles_stats", "statistic", "MONGODB/stats")
}


def message_get_stoptimes():
    message = message_creator(MESSAGES_SET["stoptimes_normal"])
    # Debug:
    # print(f"Debug: message in message_get_stoptimes:\n {message}")
    return message


def message_get_statistic():
    message = message_creator(MESSAGES_SET["statistic_normal"])
    # print(f"Debug: message in message_get_statistic:\n {message}")
    return message


def message_get_stops():
    message = message_creator(MESSAGES_SET["stoptimes_stop"][0])
    return message


def message_get_shapes():
    message = message_creator(MESSAGES_SET["stoptimes_shapes"][0])
    return message
