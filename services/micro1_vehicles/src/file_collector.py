"""
Function to download .pb files
@M-Malek
"""
import datetime
import requests
import urllib3
import time


def file_collector(url):
    """
    Download ZTM data files
    :param url: URL to file to download
    :return: ZTM server response with .pb or .zip file (depending on given url)
    """
    # variables:
    # conn_counter - counter of data download attempts
    # data - collected data file
    v_conn_counter = 1

    while v_conn_counter < 4:
        time.sleep(10)
        try:
            response = requests.get(url)
            return response
        except requests.HTTPError or urllib3.exceptions.IncompleteRead as e:
            print(f"Error at {datetime.datetime.now()}, attempt: {v_conn_counter}: {e}")
            return False