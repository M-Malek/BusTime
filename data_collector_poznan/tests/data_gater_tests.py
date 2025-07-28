from data_collector_poznan.src.gather.feeds_gater import download_vehicle_data


def download_dvd_test1():
    """
    Check if data could be downloaded
    :return:
    """
    download_vehicle_data("https://www.ztm.poznan.pl/pl/dla-deweloperow/getGtfsRtFile?file=vehicle_positions.pb")


download_dvd_test1()
