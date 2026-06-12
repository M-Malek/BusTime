from pymongo import DESCENDING


def get_latest_checksum(collection):
    latest = collection.find_one(
        sort=[("created_at", DESCENDING)]
    )
    return latest

def get_latest_checksum_data(collection):
    doc = collection.find_one(
        sort=[("created_at", DESCENDING)]
    )
    if not doc:
        return None
    checksum = doc.get("checksum")
    began_at = doc.get("began_at")
    return began_at, checksum