import zipfile
import datetime
import requests
import urllib3
import io
import time


class FilesToolBox:
    @staticmethod
    def encoding_checker(file):
        """
        Check given file encoding
        :param file: file to check
        :return: string, file encoding
        """
        import chardet
        # with open(file, 'rb') as f:
        #     result = chardet.detect(f.read())
        #     f.close()
        result = chardet.detect(file)
        # print(f"Encoding: {result}")
        return result["encoding"]

    @staticmethod
    def zip_unpacker(zip_file, file_to_find):
        """
        Unpack zip and return searched file
        :param zip_file: examined .zip file
        :param file_to_find: name of searched file
        :return:
        """
        with zipfile.ZipFile(zip_file, 'r') as zip_data:
            for file_name in zip_data.namelist():
                if file_name == file_to_find:
                    searched_file = zip_data.open(file_name)
            zip_data.close()
        return searched_file

    @staticmethod
    def read_zip(file):
        with zipfile.ZipFile(io.BytesIO(file.content), 'r') as v_zip_data:
            for file_name in v_zip_data.namelist():
                with v_zip_data.open(file_name) as raw_file:
                    file_content = raw_file.read().decode('utf-8')
                    print(f"Rows in: {file_name} file")
                    print(file_content)
                    print("--------------")
                    raw_file.close()
            v_zip_data.close()

    @staticmethod
    def file_collector(url):
        """
        Download ZTM data files
        :param url: URL to file to download
        :return: ZTM server response with .pb or .zip file (depending on given url)
        """
        # variables:
        # conn_counter - counter of data download attempts
        # data - collected data file
        v_conn_counter = 1

        while v_conn_counter < 4:
            time.sleep(10)
            try:
                response = requests.get(url)
                return response
            except requests.HTTPError or urllib3.exceptions.IncompleteRead as e:
                print(f"Error at {datetime.datetime.now()}, attempt: {v_conn_counter}: {e}")
                return False

    @staticmethod
    def log_bad_line(line):
        print(f"Error during read a line: {line}")

    @staticmethod
    def row_decoder(row):
        """
        Decode given row with data to list of all separate data
        :param row: str, string with data downloaded from .zip file
        :return: list, list of separated data
        """
        raw_data = row.split(",")
        result = []
        # Clean data
        for datum in raw_data:
            # Remove white marks
            datum.strip()
            # Remove extra quotation marks
            if datum.startswith('"') and datum.endswith('"'):
                datum = datum[1:-1]
            try:
                datum = int(datum)
            except ValueError:
                pass
            result.append(datum)

        return result


class BasicDataInformation(FilesToolBox):
    def __init__(self, file):
        self.file = io.BytesIO(file.content)
        self.type = type(self.file)


class WebSearcher:
    def __init__(self):
        pass

    @staticmethod
    def file_names_column_table_searcher(url):
        """
        Search ZTM site, find all dates with time tables .zips available to download
        :return: list, list of file names
        """
        from bs4 import BeautifulSoup
        import requests

        response = requests.get(url)
        if response.status_code == 200:
            site = BeautifulSoup(response.text, 'html.parser')
            table_loc = site.find("div", {'class': 'table-responsive'})
            table_content = table_loc.find('tbody')
            # Iterate through table_content
            # Find 'tbody' tag
            # Find 'tr' tag
            # If 'td' with file name found (.zip in name), add to result list
            searched_tds = []
            result_tuples_list = []
            # row_content = table_content.find('tr')
            td_content = table_content.findAll('td')
            for td in td_content:
                if '.zip' in td.text:
                    searched_tds.append(td)

            # From founded td tag separate dates and save in tuple (start_date, end_date)
            for datum in searched_tds:
                start_date = datum.text[0:8]
                end_date = datum.text[9:17]
                # print(start_date, end_date)
                new_tuple = (start_date, end_date)
                result_tuples_list.append(new_tuple)

            return result_tuples_list
        else:
            # There was an error during file check!
            print(f"Error: cannot check if new .zip file exist!")
            return []

    @staticmethod
    def download_old_timetable_ZTM_Poznan(*args):
        """
        Download .zip with old timetable according to given dates
        :param args: str, timetables start and end dates
        :return: .zip file with data
        """
        import requests

        if len(args) != 1:
            try:
                dates = (args[0], args[1])
            except ValueError:
                raise ValueError("Bad dates!")
        else:
            try:
                dates = args[0]
            except ValueError:
                raise ValueError("Bad dates!")

        download_url = r"https://www.ztm.poznan.pl/pl/dla-deweloperow/getGTFSFile/?file="
        downloaded_file = requests.get(download_url+dates)
        return downloaded_file


def in_time_period(time_start, time_end, time_now):
    """
    Check if given hour is in given time period
    :param time_start: start hour of time period,
    :param time_end: end hour of time period
    :param time_now: hour to check
    :return: True if time_now in given time period (time start to time_end)
    """
    # print("Debug")
    # print(f"Start time: {time_start}")
    # print(f"End time: {time_end}")
    # print(f"Now: {time_now}")
    if time_start < time_end:
        return time_start <= time_now <= time_end
    else:
        # return time_start < time_now < time_end
        return time_now >= time_start or time_now <= time_end
