from pymongo import DESCENDING


def get_latest_checksum(collection):
    latest = collection.find_one(
        sort=[("created_at", DESCENDING)]
    )
    return latest