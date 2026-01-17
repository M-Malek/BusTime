"""
Downloading .zip file from ZTM server
@M-Malek
"""
import requests
from io import BytesIO
from shared.tools.log_logging import main_logger
from requests.exceptions import HTTPError
from time import sleep


def zip_downloading(url, retrives=3, timer=10):
    """
    Download .zip file from ZTM Server
    :param url: URL to .zip file
    :param retrives: int, retrives counter - counter of times which def will try to redownload file
    "param timer: int, count of seconds to wait before next connection attempt
    :return: Bytes object (downloaded .zip file) or none if there was an error during downloading a file
    """
    for attempt in range(1, retrives+1):
        main_logger("info", f"Trying to download .zip file, attempt: {attempt}")
        # response = requests.get(url)
        try:
            response = requests.get(url)
            response.raise_for_status()
            main_logger("info", ".zip file downloaded successfully")
            return BytesIO(response.content)
            # return BytesIO(response.content)

        except requests.exceptions.ConnectionError as e:
            main_logger("error", f"Microservice 2: No internet connection or ZTM site unavailable! {e}")
            main_logger("warning", f"Retrying to download zip, attempts left: {retrives - attempt}")
            sleep(timer)
            # return zip_downloading(url, retrives - 1)

        except HTTPError as e:
            status = e.response.status_code
            if 400 <= status < 500:
                main_logger("error", f"Client side error during downloading .zip file! File not downloaded.")
                # return None
            elif 500 <= status < 599:
                main_logger("error", f"ZTM server with .zip files currently unavailable! Status code: {e}. "
                                     f"File not downloaded.")
                # return None
            else:
                main_logger("error", f"HTTPError during downloading .zip file: {e}")
                # return None
            main_logger("warning", f"Retrying to download zip, attempts left: {retrives - attempt}")
            sleep(timer)

        except requests.exceptions.RequestException as e:
            main_logger("error", f"Microservice 2: Unexpected request error:{e}")
            main_logger("warning", f"Retrying to download zip, attempts left: {retrives - attempt}")
            sleep(timer)
            # return None
    main_logger("error", "After 3 downloads attempts, .zip download failed!")
    return None
