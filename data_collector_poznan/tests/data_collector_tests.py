from data_collector_poznan.src.parser.feeds_collector import feeds_manager
import datetime
import time
from collections import defaultdict
import random


def test_1(url1, url2):
    """
    Test data downloading:
    Take one row for 10 different downloads and validate data:
    :param url1: URL for ZTM's vehicle_positions.pb
    :param url2: URL for ZTM's feeds.pb
    :return: Avg data preparation time and count of "None" - missing data
    """
    dataset = feeds_manager(url1, url2)
    for i in range(0, 3):
        test_value = random.randint(0, len(dataset))
        print(dataset[test_value])


def test_2(url1, url2):
    """
    Test data downloading:
    Run script 100 times and check if all data has been downloaded correctly.
    Count number of none
    :param url1: URL for ZTM's vehicle_positions.pb
    :param url2: URL for ZTM's feeds.pb
    :return: Avg data preparation time and count of "None" - missing data
    """
    # dataset = feeds_manager(url1, url2)
    none_counts = {}
    timestable = []
    for run in range(0, 100):
        # Measure of time:
        time1 = datetime.datetime.now()
        dataset = feeds_manager(url1, url2)
        time2 = datetime.datetime.now()
        timestable.append(time2 - time1)
        none_counts = defaultdict(int)

        for record in dataset:
            for key, value in record.items():
                if value is None:
                    none_counts[key] += 1

        print(f"Run no. {run}, data preparation time: {time2 - time1} seconds.")
        # Add to ready program: download data one per minute included time of data download and preparation!
        # time.sleep(60 - datetime.timedelta(time2 - time1).total_seconds())
        time.sleep(60)

    # Check avg. data preparation time:
    # times_sum = 0
    # for times in timestable:
    #     times_sum += times
    #
    # avg_time = times_sum / len(timestable)
    # print(f"Tests ended: avg. data preparation time: {avg_time} seconds.\n")
    for field, count in none_counts.items():
        print(f"{field}: {count} brakujących wartości (None)")


link1 = r"https://www.ztm.poznan.pl/pl/dla-deweloperow/getGtfsRtFile?file=vehicle_positions.pb"
link2 = r"https://www.ztm.poznan.pl/pl/dla-deweloperow/getGtfsRtFile?file=feeds.pb"
# test_2(link1, link2)
test_1(link1, link2)
"""
Tests result:
Test no. 1:
Check data connection in feeds_manager! 'seq' and 'delay' are often None!
-
Test no. 2:
After run 47 download_vehicle_data(url_feeds) catch error:
google.protobuf.message.DecodeError: Error parsing message with type 'transit_realtime.FeedMessage'
Solution: add protbuf.Decode check before decoding. If error during decoding - skip iteration, data corrupted
"""