"""
Log file - function to log program workflow in command line and separate files
@M-Malek
"""
from datetime import datetime


def log(message_type=0):
    """
    Log messages to command line and log file
    Log file function - work in progress
    :param log_file: file to save log information
    :param message_type: int, type message to show - check log_file for information codes
    :return:
    """

    def default_message():
        print(f"Current time: {datetime.now().time()}")

    if message_type == 0:
        default_message()
        print(f"Schedules collector collected and updated line_info, shapes and stop times!")

    elif message_type == 1:
        default_message()
        print("Vehicles positions saved to database")

    elif message_type == 2:
        default_message()
        print("No needs to update line_info, shapes and stop times")
