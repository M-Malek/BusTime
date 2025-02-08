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
