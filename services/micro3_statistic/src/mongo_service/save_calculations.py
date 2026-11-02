import os

from ztm_tools.mongo_tools.mongo_connect import create_mongo_connection
from ztm_tools.logging.logger import main_logger

def save_calculations(trip_progress):
    """Save actually calculated trip progress."""
    if trip_progress is None:
        return None

    document = trip_progress.to_dict()
    trip_id = document.get("trip_id")
    if trip_id is None:
        main_logger("error", "save_calculations: TripProgress must have trip_id")
        return None

    client = create_mongo_connection(os.getenv("MONGO_URI"))
    if client is None:
        main_logger(
            "error",
            f"save_calculations: Cannot connect to MongoDB; skipping trip_id={trip_id}",
        )
        return None

    try:
        collection = client["Poznan"]["Line_info"]
        result = collection.update_one(
            {"trip_id": trip_id},
            {"$set": document},
            upsert=True,
        )
        return result
    finally:
        client.close()
