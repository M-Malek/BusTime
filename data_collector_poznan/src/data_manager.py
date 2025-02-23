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


def download_trips_data(url):
    """
    Run functions to download data about trips from ZTM services
    :param url: url for data
    :return: None or ValueError if data download or save failed
    """
    from data_collector_poznan.src.data_preparing import ReadZipData as ReadZip
    import shared.tools.data_collector as data_collector
    import shared.tools.env_os_variables as eov
    import shared.tools.filestoolbox as FilesToolBox

    """
    ZTM save their .zip files with time tables etc. in very useful format:
    start-date_end-date.zip
    On start: extract all zip names and create a list of available files
    Once a day check file - if new file has been found, update the list and save new file and start extraction to db
    """
    # Step 1: download list:
    file_names = FilesToolBox.WebSearcher(eov.dc_zip_files_list_url).file_names_column_table_searcher('Nazwa pliku')
    print(file_names)
    # Step 2: check list:
    # Step 3 (if there is a new list) save file, start extraction to db:


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

