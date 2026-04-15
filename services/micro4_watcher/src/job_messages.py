import boto3
import json
import os
from src.sqs_messages import MESSAGES_SET, message_creator


# def message_vehicles_wipeout():
#    message_creator(MESSAGES_SET["vehicle_wipeout"][0], MESSAGES_SET["vehicle_wipeout"][1])


def message_get_stoptimes():
    message_creator(MESSAGES_SET["stoptimes_normal"][0])


def message_get_statistic():
    message_creator(MESSAGES_SET["statistic_normal"][0])


def message_get_stops():
    message_creator(MESSAGES_SET["stoptimes_stop"][0])


def message_get_shapes():
    message_creator(MESSAGES_SET["stoptimes_shapes"][0])

