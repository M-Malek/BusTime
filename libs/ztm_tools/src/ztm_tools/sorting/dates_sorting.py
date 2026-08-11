"""
Sorting algorithm for finding most matching date range
@M-Malek
"""
from datetime import datetime

# def data_range_sorter(data: str, ranges: list):
#     """
#     Find most matching date range:
#     1. Filter ranges with searched date
#     2. Filter the smallest ranges with searched date
#     3. For all the smallest ranges with searched date find one with the eldest start date
#     :param data: str, examined data
#     :param ranges: list, list of tuples. Each tuple is
#     (MongoDB entry id, string with dates in format "YYYYMMDD-YYYYMMDD")
#     :return: tuple, tuple with matching date range. If date doesn't belong to range, return tuple ("noID", "noDatesRange")
#     """
#     # 1. Filter ranges with searched date
#     # 1.1 Iterate through all ranges:
#     _result_ranges = []
#     for data_set in ranges:
#         dates = data_set[1]
#         # print(dates)
#         # 1.2.1 Convert date string to start_date and end_date
#         start_date = datetime.strptime(dates.split("-")[0], "%Y%m%d")
#         end_date = datetime.strptime(dates.split("-")[1], "%Y%m%d")
#         # print(f"{start_date} <-- {datetime.strptime(data, '%Y%m%d')} <-- {end_date}")
#         # 1.2.2 If data in range: start_date <= date <= end_date
#         if start_date <= datetime.strptime(data, "%Y%m%d") <= end_date:
#             _result_ranges.append(data_set)
#
#     #print(_result_ranges)
#     # 2. Filter the smallest range
#     # 2.1 Create date_count dict
#     # 2.2 For range in _result_ranges
#     date_count = {}
#     for r in _result_ranges:
#         dates = r[1].split("-")
#         # 2.2.1 Calculate range length
#         start_date = datetime.strptime(dates[0], "%Y%m%d")
#         end_date = datetime.strptime(dates[1], "%Y%m%d")
#         date_length = end_date - start_date
#         # 2.2.2 Add to date_count: key - range
#         date_count[r[1]] = date_length
#
#     # 3. Find matching date
#     #print(date_count)
#     # 3.1 Create best_dates dict
#     best_dates = []
#     # 3.2 Find lowest value in date_count
#     # Fuse: if our data is not connected with ranges - result doesn't exist.
#     try:
#         lowest_days_range = min(list(date_count.values()))
#     except ValueError:
#         # There is no range for this date
#         result = ("noID", "noDatesRange")
#         return result
#     # 3.3 Find all ranges with this value
#     #print(lowest_days_range)
#     for lowest_range in list(date_count.keys()):
#         # print(f"{lowest_range}: {date_count[lowest_range]}")
#         if date_count[lowest_range] == lowest_days_range:
#             best_dates.append(lowest_range)
#     # 3.4 Find range with the highest start date (first date in a row)
#     # print(best_dates)
#     lowest_start_date = datetime.strptime(best_dates[0].split("-")[0], "%Y%m%d")
#     winner_date_range = ""
#     for date in best_dates:
#         if lowest_start_date <= datetime.strptime(date.split("-")[0], "%Y%m%d"):
#             lowest_start_date = datetime.strptime(date.split("-")[0], "%Y%m%d")
#             winner_date_range = date
#     # print(lowest_start_date)
#
#     # 3.5 Return id of this range (range converted to str) and range
#     # how to make a return statement? ranges is a list of tuples: tuple has mongo_micro_tools id and name with dates
#     # I need to search these tuples for proper range
#     # Return must return list with the smallest start date and the smallest timedelta
#     ranges_by_data_range = {data_range: item for item, data_range in ranges}
#     # print(ranges_by_data_range)
#     # result_list = [entry for entry in ranges if datetime.strptime(entry[1].split("-")[0], "%Y%m%d") ==
#     #                lowest_start_date]
#     result_list = [entry for entry in ranges if entry[1] == winner_date_range]
#     #print(f"Result: {result_list[0]}")
#     return result_list[0]
#     # Function tested - bad logic!

def data_range_sorter(data: str, ranges: list):
    """
    Find the most suitable date range for a given date.

    The suitable range is the one that:
    1. contains the examined date,
    2. has the latest start date among all matching ranges.

    :param data: str, examined date in format "YYYYMMDD"
    :param ranges: list of tuples:
        (MongoDB entry id, "YYYYMMDD-YYYYMMDD")
    :return: matching tuple or ("noID", "noDatesRange")
    """

    examined_date = datetime.strptime(data, "%Y%m%d")

    matching_ranges = []

    for data_set in ranges:
        start_date, end_date = (
            datetime.strptime(date, "%Y%m%d")
            for date in data_set[1].split("-")
        )

        if start_date <= examined_date <= end_date:
            matching_ranges.append(
                (data_set, start_date, end_date)
            )

    if not matching_ranges:
        return ("noID", "noDatesRange")

    # Find ranges with the latest start date
    latest_start_date = max(
        x[1] for x in matching_ranges
    )

    same_start_ranges = [
        x for x in matching_ranges
        if x[1] == latest_start_date
    ]

    # If several ranges have the same start date,
    # choose the one with the earliest end date
    winner = min(
        same_start_ranges,
        key=lambda x: x[2]
    )

    return winner[0]
