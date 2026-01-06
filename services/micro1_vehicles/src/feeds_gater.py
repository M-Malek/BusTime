"""
Download feed files for next processing
Creator: M-Malek
"""
from google.protobuf.message import DecodeError
import shared.tools.filestoolbox as FilesToolBox
from google.transit import gtfs_realtime_pb2
from shared.tools.log_logging import main_logger


def download_vehicle_data(url):
    """
    Run functions to download data about trips from ZTM services (download feeds.pb)
    :param url: url for data
    :return: data: GFTS raw data in ... format or None if data download failed
    """
    # import shared.tools.filestoolbox as FilesToolBox
    # from google.transit import gtfs_realtime_pb2
    # from google.protobuf.json_format import MessageToDict

    # 1. Download feeds.pb
    raw_data = FilesToolBox.FilesToolBox.file_collector(url)

    # 2. Encode feeds.pb
    try:
        data = gtfs_realtime_pb2.FeedMessage()
        data.ParseFromString(raw_data.content)
        # Debug:
        # print(type(data))
        # data expression type: gtfs_realtime_pb2.FeedMessage
    except DecodeError:
        main_logger("error", "Decoding error after downloading protbuf file from ZTM services!")
        return None

    return data



