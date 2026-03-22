"""
Detect new stop time on ZTM Poznań website
@M-Malek
"""
import os

import requests
import hashlib
import re
from pymongo import MongoClient, DESCENDING
from datetime import datetime
from src.log_logging import main_logger

"""
4 steps:
1 step - check ZTM site, download file, create file checksum
2 step - download last checksum from MongoDB collection
3 step - compare new checksum with checksum from MongoDB collection
4 step - if checksums are equal, skip, else: set new SQS messages for another microservices
"""


def checksum_creator():
    url = os.getenv("ZTM_URL")

    response = requests.get(url)
    response.raise_for_status()

    hash = hashlib.sha256()

    # 1 step - creating checksum and file information
    # Create checksum
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            hash.update(chunk)

    checksum = hash.hexdigest()

    # Read filename from response headers - Content-Disposition
    content_disposition = response.headers.get("Content-Disposition")

    if content_disposition:
        match = re.search(r'filename="?([^"]+)"?', content_disposition)
        if match:
            file_name = match.group(1)
        else:
            file_name = "unknown.zip"
    else:
        file_name = "unknown.zip"

    return checksum, file_name


def get_latest_checksum(collection):
    latest = collection.find_one(
        sort=[("created_at", DESCENDING)]
    )
    return latest


def checksum_compare(checksum_new, checksum_old):
    if checksum_new == checksum_old:
        return True
    else:
        return False


def checksum_checker():

    new_checksum, file_name = checksum_creator()
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["Poznan"]
    collection = db["Stop_times_arch"]
    last_checksum = get_latest_checksum(collection)

    if not checksum_compare(new_checksum, last_checksum):
        # There is new checksum - new .zip file on ZTM server detected
        main_logger("info", "New file on ZTM server detected!")
        collection.insert_one({
            "checksum": new_checksum,
            "file_name": file_name,
            "created_at": datetime.utcnow()
        })
        client.close()
        return True
    else:
        main_logger("info", "There isn't new .zip file")
        client.close()
        return False
