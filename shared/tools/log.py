"""
Log file - function to log program workflow in command line and separate files
@M-Malek
"""
from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


def log(message_type=0):
    """
    Log messages to command line and log file
    Log file function - work in progress
    :param log_file: file to save log information
    :param message_type: int, type message to show - check log_file for information codes
    :param own_message: str, custom message to shown
    :return:
    """
    message = ""

    def default_message(with_db_log=False):
        time_message = f"Current time: {datetime.now().time()}"
        print(time_message)
        if with_db_log:
            return time_message

    if message_type == 0:
        default_message()
        print(f"Schedules collector collected and updated line_info, shapes and stop times!")

    elif message_type == 1:
        default_message()
        print("Vehicles positions saved to database")

    elif message_type == 2:
        default_message()
        print("No needs to update line_info, shapes and stop times")


def db_logger(uri, log_type, log_mess):
    """
    Function to log and check, if data has been saved in DB
    :param uri: MongoDB Client URI (URI for db with collection Logs to data save
    :param log_type:  logging message type: two possible options: normal/error
    :param log_mess:  log message which will be save in database
    :return: error log if data check failed
    """
    if log_type not in ["normal", "error"]:
        raise Exception("Incorrect log type")
        pass

    time = datetime.now()
    if log_type == "normal":
        ready_message = log_mess
    if log_type == "error":
        ready_message = "Error with: " + log_mess

    try:
        client = MongoClient(uri, server_api=ServerApi('1'))
        db_set = client["Poznan"]
        collection = db_set["Logs"]
        collection.insert_one(
            {
                "log_time": time,
                "log_type": log_type,
                "log_message": ready_message
            }
        )
        client.close()
        print(f"{time}: " + ready_message)
    except Exception as e:
        print("An error during a connection: " + str(e))
        return False


def txt_logger(message):
    """
    Save log message to file log.txt in default microservice folder
    :param message:
    :return:
    """
    pass
