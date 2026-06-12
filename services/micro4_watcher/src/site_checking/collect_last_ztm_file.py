import os
import requests
import hashlib
from src.site_checking.zip_filename_reader import filename_reader
from io import BytesIO


def collect_last_ztm_file(url):
    """
    Collects the latest ZTM file
    :return: content: requests.response.content object, file_name: string
    """
    # url = os.getenv("ZTM_URL")
    # print(url)
    response = requests.get(url)

    #response.raise_for_status()

    content = response.content
    file_name = filename_reader(BytesIO(content))

    return response, file_name