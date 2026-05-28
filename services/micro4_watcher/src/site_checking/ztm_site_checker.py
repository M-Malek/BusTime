"""
Detect new stop time on ZTM Poznań website
@M-Malek
"""
import os

from pymongo import MongoClient
from datetime import datetime
from src.log_logging import main_logger
from src.site_checking.checksum_creator import checksum_creator
from src.site_checking.get_last_checksum import get_latest_checksum
from src.site_checking.checksum_compare import checksum_compare

"""
4 steps:
1 step - check ZTM site, download file, create file checksum
2 step - download last checksum from MongoDB collection
3 step - compare new checksum with checksum from MongoDB collection
4 step - if checksums are equal, skip, else: set new SQS messages for another microservices
"""

def checksum_checker():
    """
    Check hash.sha256() sum's of zip files: already stored in Mongo and from ZTM website
    :return: True if there is a new .zip file detected on ZTM website, else False
    """
    # print("Debug: this checksum_checker is running!")
    new_checksum, file_name = checksum_creator()
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["Poznan"]
    collection = db["Stop_times_arch"]
    # Debug:
    try:
        last_checksum = dict(get_latest_checksum(collection))['checksum']
        # print(f"Debug in checksum_checker: last checksum from MongoDB: {last_checksum}")
    except TypeError as e:
        # If TypeError occurred: there is no data about last .zip file. Checksum hasn't been created yet
        main_logger("warning", "There is no data about last .zip file in MongoDB collection. Checksum hasn't been created yet.")
        last_checksum = 0
        # So program will create something (it doesn't care what) to achieve running of checksum_compare below"
    # print(f"old checksum: {last_checksum}, type: {type(last_checksum)}")
    # print(f"new checksum {new_checksum}, type: {type(new_checksum)}")
    # print(f"Debug: name of file: {file_name}")
    # print(f"Debug in checksum_compare: new checksum: {new_checksum}, old checksum: {last_checksum}")
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
