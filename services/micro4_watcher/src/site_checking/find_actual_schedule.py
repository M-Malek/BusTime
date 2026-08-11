"""
Compare dates of entries and current date to examine, if we have new actual vehicles schedule
@M-Malek
"""
from ztm_tools.mongo_tools.mongo_connect import create_mongo_connection
from ztm_tools.sorting.dates_sorting import data_range_sorter
from os import getenv
from datetime import datetime, timedelta

def find_actual_schedule():
    """
    Find actual schedule
    :return: tuple: data of entry actual for today, format: (Mongo Collection _id, file_name date)
    """
    # 1. Create connection with collection
    connection = create_mongo_connection(getenv("MONGO_URI"))
    collection = connection["Poznan"]["Stop_times_arch"]
    # 2. Get all collection entries sorted descending by created_at with today's date
    today_for_mongo_str = datetime.strftime(datetime.now(), "%Y%m%d")
    #all_entries = collection.find({"state": "active"})
    #all_entries = collection.find({"state": "pending"})
    all_entries = collection.find({})
    examined_entries = []
    for e in all_entries:
        if datetime.strptime(e["began_at"], "%Y%m%d") >= datetime.now() - timedelta(days=30):
            examined_entries.append(e)
    # 3. Prepare data from all_entries to process by data_range_sorter:
    all_entries_prepared = []
    for entry in examined_entries:
        data_range = entry["file_name"].replace("_", "-")
        all_entries_prepared.append((entry["_id"], data_range))
    # last actual entry - an entry which matches today's date
    # connection.close()
    # print(all_entries_prepared)
    # print(all_entries_prepared)
    last_actual_entry = data_range_sorter(today_for_mongo_str, all_entries_prepared)
    # 4. Return id of founded entry
    if last_actual_entry == ("noID", "noDatesRange"):
        # There is no new schedule which should be active so this one with state = "active" is valid
        winner = collection.find_one({"state": "active"})
        result_winner = (winner["_id"], winner["file_name"])
        connection.close()
        return result_winner
    else:
        # print(f"Debug: last actual entry {last_actual_entry[0]}")
        #return last_actual_entry[0] # it should return tuple with id of entry closest to today date
        connection.close()
        return last_actual_entry

"""
Last acutal entry - to wpis który pasuje do zamierzeń dzisiejsza data i przedziały tj.:
Jeżeli jest kilka wpisów w MongoDB które mają przedział dat z dzisiejszą datą, np. 20260610-20260617, 20260612-20260621,
20260612-20260613 a dzisiaj jest 12 czerwca (czyli 20260612 w zapisie daty Mongo) to muszę znaleźć ten przedział dat,
który jak najbardziej spełnia moje kryterium czasowe - w tym przypadku jest to zwykle najmniejszy przedział czasu
zawierający moją datę. Kod funkcji musi znajdować ten przedział.
"""

