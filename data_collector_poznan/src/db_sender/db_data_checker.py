"""
Function to verify if timetable database required to be updated
@M-Malek
"""
import data_collector_poznan.src.db_sender.data_sender as db_sender
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


def download_probe(uri):
    if not db_sender.connection_checker(uri):
        print("Database currently unavailable. Probe download failed")
        return None

    client = MongoClient(uri, server_api=ServerApi('1'))
    db_set = client["Poznan"]
    pass
