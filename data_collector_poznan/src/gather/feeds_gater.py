"""
Download feed files for next processing
Creator: M-Malek
"""
import google

# GLOBALS:


def download_vehicle_data(url):
    """
    Run functions to download data about trips from ZTM services (download feeds.pb)
    :param url: url for data
    :return: data: GFTS raw data in ... format or None if data download failed
    """
    import shared.tools.filestoolbox as FilesToolBox
    from google.transit import gtfs_realtime_pb2
    from google.protobuf.json_format import MessageToDict

    # 1. Download feeds.pb
    raw_data = FilesToolBox.FilesToolBox.file_collector(url)

    # 2. Encode feeds.pb
    try:
        data = gtfs_realtime_pb2.FeedMessage()
        data.ParseFromString(raw_data.content)
        # Debug:
        # print(type(data))
        # data expression type: gtfs_realtime_pb2.FeedMessage
    except google.protobuf.message.DecodeError:
        return None

    return data

    # 3. Prepare feeds.pb - extract only requested data
    # Data extracted from feeds.pb file
    """
    {
    "vehicle_id": "505",
    "trip_id": "T12_20250624_001",
    "timestamp": "2025-06-24T08:07:30Z",
    "lat": 52.4123,
    "lng": 16.9312,
    "delay_seconds": 120
    }
    Wygląd pojedynczego wpisu pojazdu
    entity {
    id: "8323"
    trip_update {
        trip {
            trip_id: "5_2751480^+"
            schedule_relationship: SCHEDULED
            route_id: "835"
            }
    stop_time_update {
      stop_sequence: 4
      arrival {
        delay: 263
      }
      schedule_relationship: SCHEDULED
        }
    vehicle {
      id: "8323"
      label: "835/22"
    }
    timestamp: 1751301778
    }
    }

    """


