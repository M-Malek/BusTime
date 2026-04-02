"""
Reade name of .zip file to save with hash checksum in MongoDB.
This option is needed to check, if we have to download new data to S3.
@M-Malek
"""
from zipfile import ZipFile
import io
from pandas import DataFrame, read_csv


def filename_reader(response):
    # Debug:
    print(response.status_code)
    print(response.headers.get("Content-Type"))
    print(response.content[:200])
    zip_file = ZipFile(io.BytesIO(response.content))

    # Otwórz calendar.txt
    with zip_file.open("calendar.txt") as file:
        dates_dataframe = read_csv(file)
        print(dates_dataframe)
        file.close()

    return "None - already"
