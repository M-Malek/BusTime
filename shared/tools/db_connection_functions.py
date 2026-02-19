"""
Functions to connect with MongoDB database
"""
import os

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from shared.tools.log_logging import main_logger
from pymongo.errors import ConnectionFailure


def connection_establisher():
    """
    Check and establish connection with given MongoDB database
    :param uri: MongoDB uri
    :return: connected MongoDB client
    """
    uri = os.getenv("MONGO_URI")
    try:
        client = MongoClient(uri, server_api=ServerApi('1'))
        client.admin.command('ping')
        return client
    except ConnectionFailure as e:
        main_logger("error", f"Connection with MongoDB cannot be established: {e}")
        return None
    except Exception as e:
        main_logger("error", f"Error during connection with MongoDB: {e}")
        return None
