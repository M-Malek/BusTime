import os
import time

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_gtfs_files():
    """
    Collect all URL's on ZTM site and create of dict: {date: url}
    :return: dict: {date: url} with all URL's on ZTM site
    """
    def try_connection(ztm_url):
        repeat = True
        while repeat:
            try:
                ztm_response = requests.get(ztm_url, timeout=10)
                ztm_response.raise_for_status()
                repeat = False
            except requests.exceptions.ConnectionError:
                continue
        return ztm_response

    url = os.getenv("ZTM_ZIP_URL_LIST")
    response = try_connection(url)

    soup = BeautifulSoup(response.text, "html.parser")

    files = []

    # Find all links on ZTM site
    for link in soup.find_all("a"):
        href = link.get("href")
        text = link.get_text(strip=True)

        # If link is not href, skip
        if not href:
            continue

        # Find all links
        if ".zip" in href.lower():
            # Create URL
            full_url = urljoin(url, href)
            # Extract URL on 3 parts
            before, key, after = full_url.partition("?file=")

            # Extract date from URL and save in pairs in files list
            files.append({
                "name": after.split(".")[0],
                "url": full_url
            })

    # Return dict with pairs date: url
    return {item["name"]: item["url"] for item in files}
