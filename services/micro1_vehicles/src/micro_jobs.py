"""
Micro1 jobs file
@M-Malek
"""
from src.collector_runner import vehicles
# from services.micro1_vehicles.src.data_sender import connection_establisher
from src.data_sender import connection_establisher
# from shared.tools.env_os_variables import db_uri
import os
from src.log_logging import main_logger


def job_data_download():
    """while True:
        client = connection_establisher(db_uri)
        vehicles()
        client.close()
        sleep(30)"""
    # client = connection_establisher(db_uri)
    client = connection_establisher(os.getenv("MONGO_URI"))
    if client is None:
        main_logger("error", "Cannot complete job_data_download! Data skipped.")
    else:
        vehicles(client)
        client.close()
    # sleep(30)


def job_database_wipeout():
    """if not connection_checker(uri):
        # print("Database currently unavailable. Data wipeout failed")
        main_logger("error", "Database currently unavailable. Data wipeout failed")
        return None"""

    client = connection_establisher(os.getenv("MONGO_URI"))
    tables = ["Vehicle"]
    # print(f"Starting data wipeout from collections: {tables}")
    main_logger("warning", f"Starting data wipeout from collections: {tables}")
    # client = MongoClient(uri, server_api=ServerApi('1'))
    db_set = client["Poznan"]
    for table in tables:
        # Debug:
        # print(f"{table} type: {type(table)}")
        collection = db_set[table]
        collection.drop()
    # client.close()
    # print(f"Data wipe outed!")
    main_logger("warning", "Vehicles data wipeouted!")
