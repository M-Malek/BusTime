"""
Log file - function to log program workflow in command line and separate files
@M-Malek
"""
from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import logging


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
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO)

    def default_message(with_db_log=False):
        time_message = f"Current time: {datetime.now().time()}"
        print(time_message)
        if with_db_log:
            return time_message

    if message_type == 0:
        time_mes = default_message(with_db_log=True)
        message = f"Schedules collector collected and updated line_info, shapes and stop times!"
        logger.info(time_mes + message)

    elif message_type == 1:
        time_mes = default_message(with_db_log=True)
        message = "Vehicles positions saved to database"
        logger.info(time_mes + message)

    elif message_type == 2:
        time_mes = default_message(with_db_log=True)
        message = "No needs to update line_info, shapes and stop times"
        logger.info(time_mes + message)


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


def main_logger(message_type, message_body):
    """
    Save log message to .log file in default microservice folder
    :param message: str, message for logger
    :return: logging service status
    """
    # Create logger object
    logger = logging.getLogger()
    logging.basicConfig(filename="log_file.log",
                        format='%(asctime)s: %(levelname)s: %(message)s',
                        level=logging.INFO)

    # Create logger object body based on information given by user. Save info in file and print it to console
    if message_type == "warning":
        logger.warning(message_body)
        logging.warning(message_body)
    if message_type == "info":
        logger.info(message_body)
        logging.info(message_body)
    if message_type == "error":
        logger.error(message_body)
        logging.error(message_body)
    if message_type == "crit":
        logger.critical(message_body)
        logging.critical(message_body)
