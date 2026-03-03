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