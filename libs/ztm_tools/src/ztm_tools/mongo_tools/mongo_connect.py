"""Create connection with MongoDB"""
from pymongo import MongoClient
from ztm_tools.logging.logger import main_logger
from time import sleep

def create_mongo_connection(uri):
    attempts = 0

    while attempts <= 3:
        try:
            client = MongoClient(uri)
            return client
        except Exception as e:
            main_logger("error", f"Cannot connect to MongoDB: {e}. \n "
                                 f"Attempts left: {3-attempts}")
        attempts += 1
        sleep(10)

    main_logger("error", "After 3 attempts: Cannot connect to MongoDB")
    return None


