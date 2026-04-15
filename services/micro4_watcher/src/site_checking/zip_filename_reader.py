"""
Reade name of .zip file to save with hash checksum in MongoDB.
This option is needed to check, if we have to download new data to S3.
@M-Malek
"""
from zipfile import ZipFile
import io
from pandas import read_csv


def filename_reader(data):
    # Debug:
    # zip_file = ZipFile(io.BytesIO(response.content))
    zip_file = ZipFile(data)
    # Otwórz calendar.txt
    with zip_file.open("calendar.txt") as file:
        dates_dataframe = read_csv(file)
        start_date = dates_dataframe["start_date"][0]
        end_date = dates_dataframe["end_date"][0]
        file.close()
        return f"{start_date}-{end_date}"

