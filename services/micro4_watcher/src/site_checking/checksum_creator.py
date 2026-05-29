import os
import requests
import hashlib
from src.site_checking.zip_filename_reader import filename_reader
from io import BytesIO


def checksum_creator():
    url = os.getenv("ZTM_URL")

    response = requests.get(url)

    #response.raise_for_status()

    content = response.content
    hash_obj = hashlib.sha256()
    file_name = filename_reader(BytesIO(content))

    # 1 step - creating checksum and file information
    # Create checksum
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            hash_obj.update(chunk)

    checksum = hash_obj.hexdigest()

    return checksum, file_name
