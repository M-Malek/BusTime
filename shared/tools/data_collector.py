"""
data_collector.py - data collector file
Main goal: collect files with MPK/ZTM data, data download error providing
@created: M-Malek
"""
import time
import requests
import urllib3
import datetime

# GLOBALS
# PATH - path to .zip archive
# DST - Download Sleep Time - time to wait before next data download attempt from outside source
# ZIP_URL - URL to ZTM zip archive
import shared.tools.env_os_variables as env_os_variables
PATH = env_os_variables.dc_path
DST = 10
ZIP_URL = env_os_variables.dc_zip_url


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
        time.sleep(DST)
        try:
            response = requests.get(url)
            return response
        except requests.HTTPError or urllib3.exceptions.IncompleteRead as e:
            print(f"Error at {datetime.datetime.now()}, attempt: {v_conn_counter}: {e}")
            return False


def download_zip(url):
    downloaded_file = file_collector(url)
    # Save .zip to archive
    # save_zip(downloaded_file)
    return downloaded_file


def save_zip(downloaded_zip):
    save_path = PATH + r"" + "--" + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + ".zip"
    with open(save_path, 'wb') as file_location:
        file_location.write(downloaded_zip.content)


def download_feed(url):
    return file_collector(url)


# url_test = env_os_variables.dc_url_test
# download_zip(url_test)

"""
Nowe błędy do złapania przy pobieraniu danych:
.zip -> wykonać też dla feeds.pb
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='www.ztm.poznan.pl', port=443): Max retries exceeded

"""
