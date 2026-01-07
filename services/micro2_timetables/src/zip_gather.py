"""
Downloading .zip file from ZTM server
@M-Malek
"""
import requests
from io import BytesIO
from shared.tools.log_logging import main_logger


def zip_downloading(url):
    """
    Download .zip file from ZTM Server
    :param url: URL to .zip file
    :return: Bytes object (downloaded .zip file) or none if there was an error during downloading a file
    """
    response = requests.get(url)
    try:
        main_logger("info", ".zip file downloaded successfully")
        return BytesIO(response.content)

    except response.status_code != 200 or requests.exceptions.HTTPError() as e:
        if 400 <= response.status_code < 500:
            main_logger("error", f"Client side error during downloading .zip file: {e}! File not downloaded.")
        if 500 <= response.status_code < 599:
            main_logger("error", f"ZTM server with .zip files currently unavailable! Status code: {e}. "
                                 f"File not downloaded.")

        if requests.exceptions.HTTPError():
            main_logger("error", f"HTTPError during downloading .zip file: {e}")

        return None

