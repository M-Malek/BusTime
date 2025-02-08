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
    import shared.tools.data_collector as test_dc


    pass


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

