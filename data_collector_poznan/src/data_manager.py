"""
Prepare all file sets to save in database
Creator: M-Malek
"""

"""
Things required to save in database:
Vehicles:
Number
PlannedTrip ID
Lat
Lng

Stops:
Stop_id
Name
Lat
Lng
Zone

Scheduled_Route:
Route_ID
Short_Name
Type
Stops in format:
Stop_id, arrival_time, departure_time
First_stop_id
Last_stop_id

Real_Route:
Route_ID
Short_Name
Vehicle Number
Stops in format:
Stop_id, real_arrival_time, real_departure_time

Data for Vehicles, Stops and Scheduled Route are the data from vehicles.pb and .zip file
Data for Real_Route have to be calculate based on real vehicle position, actual time, stop position and scheduled 
arrival time
"""


def download_trips_data(url, archive_loc):
    """
    Run functions to download data about trips from ZTM services
    :param url: url for data
    :param archive_loc: str, location of archive folder
    :return: None or ValueError if data download or save failed
    """
    from data_collector_poznan.src.data_preparing import ReadZipData as ReadZip
    import shared.tools.data_collector as data_collector
    import shared.tools.env_os_variables as eov
    import shared.tools.filestoolbox as FilesToolBox
    import os
    import requests

    """
    ZTM save their .zip files with time tables etc. in very useful format:
    start-date_end-date.zip
    On start: extract all zip names and create a list of available files
    Once a day check file - if new file has been found, update the list and save new file and start extraction to db
    """
    # Step 1: download list:
    url_zip_link = r'https://www.ztm.poznan.pl/otwarte-dane/gtfsfiles/'
    file_names = FilesToolBox.WebSearcher.file_names_column_table_searcher(url_zip_link)
    # Step 2: check list with already downloaded files:
    files_in_dir = [f for f in os.listdir(url) if os.path.isfile(os.path.join(archive_loc, f))]
    # Step 3: if given .zip file is not in our archive_loc, download it and save in archive_loc
    for file in file_names:
        if file in files_in_dir:
            continue
        else:
            response = requests.get(url)
            if response.status_code == 200:
                with open(archive_loc, 'wb') as save_file:
                    for chunk in response.iter_content(chunk_size=1024):
                        save_file.write(chunk)
                print(f"Pobrano plik: {file}")
            else:
                print(f"Error during .zip download, error code: {response.status_code}")
                # raise requests.exceptions.HTTPError("Error during file download")
    # Step 4 (if there is a new list) save file, start extraction to db:



def download_vehicle_data(url):
    """
    Run functions to download data about trips from ZTM services
    :param url: url for data
    :return: None or ValueError if data download or save failed
    """
    pass


def trips_data_checker(url):
    """
    Check date of last .zip with trips information. If new file has been detected, download it to server
    :param url: url for data
    :return: None or Error if data download failed
    """

