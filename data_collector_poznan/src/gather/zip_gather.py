"""
Downloading .zip with routes data
@M-Malek
"""
import requests

import shared.tools.env_os_variables as env_variables
import io

# GLOBALS:
ROUTES_ARCHIVE = env_variables.route_archives


def download_trips_data(url, archive_loc=None):
    """
    Run functions to download data about trips from ZTM services
    WARNING: works only if ReadZip class is still in project!
    :param url: url for data
    :param archive_loc: str, location of archive folder
    :return: None or ValueError if data download or save failed
    """
    from data_collector_poznan.src.data_preparing import ReadZipData as ReadZip
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
    url_zip_link = env_variables.all_urls_link
    file_names = FilesToolBox.WebSearcher.file_names_column_table_searcher(url_zip_link)
    # Step 2: check list with already downloaded files:
    if archive_loc is not None:
        files_in_dir = [f for f in os.listdir(archive_loc) if os.path.isfile(os.path.join(archive_loc, f))]
    # Step 3 (if archive_loc != None: if given .zip file is not in our archive_loc, download it and save in archive_loc
        for file in file_names:
            if file in files_in_dir:
                continue
            else:
                response = requests.get(url)
                if response.status_code == 200:
                    with open(archive_loc, 'wb') as save_file:
                        for chunk in response.iter_content(chunk_size=1024):
                            save_file.write(chunk)
                    print(f"Downloaded a file: {file}")
                    new_data = ReadZip(response.content).read_data_from_zip()
                    return new_data
                else:
                    print(f"Error during .zip download, error code: {response.status_code}")
                    new_data = None
                    raise requests.exceptions.HTTPError("Error during file download")
    else:
        # archive_loc is None and app doesn't have archive loc
        response = requests.get(url)
        if response.status_code == 200:
            new_data = response
            return new_data
        else:
            print(f"Error during .zip download, error code: {response.status_code}")
            new_data = None
            raise requests.exceptions.HTTPError("Error during file download")
    # Step 4 (if there is a new list) save file, start extraction to db:
    # This step should be made with step no. 3 - new file after save need to be sent to db


def schedules_downloader(url):
    """
    Download .zip, throw error if .zip download failure
    :param url: link to URL with data
    :return: downloaded data as ???
    """
    response = requests.get(url)
    if response.status_code == 200:
        return io.BytesIO(response.content)
        # return response.content
    else:
        raise requests.exceptions.HTTPError()

