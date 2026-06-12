import os

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_gtfs_files():
    url = os.getenv("ZTM_ZIP_URL_LIST")
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    files = []

    # Szukamy wszystkich linków na stronie
    # (bo ZTM często zmienia strukturę tabel)
    for link in soup.find_all("a"):
        href = link.get("href")
        text = link.get_text(strip=True)

        if not href:
            continue

        # filtrujemy tylko zipy GTFS
        if ".zip" in href.lower():
            full_url = urljoin(url, href)
            before, key, after = full_url.partition("?file=")

            files.append({
                "name": after.split(".")[0],
                "url": full_url
            })

    return {item["name"]: item["url"] for item in files}
