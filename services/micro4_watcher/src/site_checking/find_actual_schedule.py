"""
Compare dates of entries and current date to examine, if we have new actual vehicles schedule
@M-Malek
"""
from ztm_tools.mongo_tools.mongo_connect import create_mongo_connection
from ztm_tools.sorting.dates_sorting import data_range_sorter
from os import getenv
from datetime import datetime

def find_actual_schedule():
    # 1. Create connection with collection
    connection = create_mongo_connection(getenv("MONGO_URI"))
    collection = connection["Poznan"]["Stop_times_arch"]
    # 2. Get all collection entries sorted descending by created_at with today's date
    today_for_mongo_str = datetime.strftime(datetime.now(), "%Y%m%d")
    all_entries = collection.find_all()
    # print(all_entries)
    # 3. Iterate through all entries and find id of last actual entry
    # last actual entry - an entry which matches today's date
    last_actual_entry = data_range_sorter(today_for_mongo_str, all_entries)
    connection.close()
    # 4. Return id of founded entry
    return last_actual_entry[0] # it should return url from entry with status equals to active!

"""
Last acutal entry - to wpis który pasuje do zamierzeń dzisiejsza data i przedziały tj.:
Jeżeli jest kilka wpisów w MongoDB które mają przedział dat z dzisiejszą datą, np. 20260610-20260617, 20260612-20260621,
20260612-20260613 a dzisiaj jest 12 czerwca (czyli 20260612 w zapisie daty Mongo) to muszę znaleźć ten przedział dat,
który jak najbardziej spełnia moje kryterium czasowe - w tym przypadku jest to zwykle najmniejszy przedział czasu
zawierający moją datę. Kod funkcji musi znajdować ten przedział.
"""

