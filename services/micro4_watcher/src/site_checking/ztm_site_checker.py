"""
Detect new stop time on ZTM Poznań website
@M-Malek
"""
import os

import requests
import hashlib
from io import BytesIO
import re
from pymongo import MongoClient, DESCENDING
from datetime import datetime
from src.log_logging import main_logger
from src.site_checking.zip_filename_reader import filename_reader

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
    file_name = filename_reader(BytesIO(response.content))

    # 1 step - creating checksum and file information
    # Create checksum
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            hash.update(chunk)

    checksum = hash.hexdigest()

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
    """
    Check hash.sha256() sum's of zip files: already stored in Mongo and from ZTM website
    :return: True if there is a new .zip file detected on ZTM website, else False
    """
    new_checksum, file_name = checksum_creator()
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["Poznan"]
    collection = db["Stop_times_arch"]
    # Debug:
    try:
        last_checksum = dict(get_latest_checksum(collection))['checksum']
    except TypeError as e:
        # If TypeError occurred: there is no data about last .zip file. Checksum hasn't been created yet
        last_checksum = 0
        # So program will create something (it doesn't care what) to achieve running of checksum_compare below"
    # print(f"old checksum: {last_checksum}, type: {type(last_checksum)}")
    # print(f"new checksum {new_checksum}, type: {type(new_checksum)}")
    # print(f"Debug: name of file: {file_name}")
    print(f"Debug in checksum_compare: new checksum: {new_checksum}, old checksum: {last_checksum}")
    if checksum_compare(new_checksum, last_checksum):
        main_logger("info", "There isn't new .zip file")
        client.close()
        return False

    else:
        # There is new checksum - new .zip file on ZTM server detected
        main_logger("info", "New file on ZTM server detected!")
        collection.insert_one({
            "checksum": new_checksum,
            "file_name": file_name,
            "created_at": datetime.utcnow()
        })
        client.close()
        return True
