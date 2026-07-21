from datetime import date

"""from pymongo import MongoClient
import os
from datetime import datetime, timezone
from src.site_checking.get_last_checksum import get_latest_checksum_data
from src.site_checking.collect_last_ztm_file import collect_last_ztm_file
from trash.checksum_compare import checksum_compare
from trash.calculate_checksum import calculate_checksum
from src.site_checking.ztm_site_zip_checker import fetch_gtfs_files
from src.site_checking.mongo_entry_creator import entry_creator
from ztm_tools.logging.logger import main_logger

def last_ztm_zip():
    zip_files = fetch_gtfs_files()

    today = date.today()
    # today = datetime.strptime("20260602","%Y%m%d").date()
    matching_dates = []
    for dates in list(zip_files.keys()):
        date_start = datetime.strptime(dates.split("_")[0], "%Y%m%d").date()
        date_end = datetime.strptime(dates.split("_")[1], "%Y%m%d").date()
        if date_start <= today <= date_end:
            # print(f"Te daty pasują do zakresu 02.06: {dates}")
            matching_dates.append(dates)

    if matching_dates:
        best_dates = max(matching_dates, key=lambda x: x[0])
        #print(best_dates)
        #print(zip_files[best_dates])
        return zip_files[best_dates]
    else:
        return None"""
from src.site_checking.collect_last_ztm_file import collect_last_ztm_file
from ztm_tools.logging.logger import main_logger
from src.site_checking.get_last_checksum import get_latest_checksum_data
from datetime import datetime, timezone
from src.site_checking.calculate_checksum import calculate_checksum
from pymongo import MongoClient
from src.site_checking.checksum_compare import checksum_compare
from src.site_checking.mongo_entry_creator import entry_creator
import os
from src.site_checking.last_ztm_zip import last_ztm_zip

def ztm_site_checker():

    current_zip_url = last_ztm_zip() # What happened with this function? Its gives an url for data download!
    if current_zip_url is None:
        print("No new checksum")
        # return False
    main_logger("info", "Checking ZTM site. Looking for new file with data")
    content, filename = collect_last_ztm_file(current_zip_url)
    client = MongoClient(os.getenv("MONGO_URI"))
    collection = client["Poznan"]["Stop_times_arch"]

    last_began_at, last_checksum = get_latest_checksum_data(collection)
    new_checksum = calculate_checksum(content)
    if checksum_compare(new_checksum, last_checksum):
        # Founded new data with schedule (stops times). Adding to MongoDB collection
        new_began_at = filename.split("-")[0]
        created_at = datetime.now(timezone.utc)
        entry_creator(collection=collection, new_checksum=new_checksum, filename=filename, created_at=created_at,
                      began_at=new_began_at, url=current_zip_url, state="pending")
        main_logger("info", "Detected new file on ZTM site, saved info in database")
        client.close()
        return True
        # return {"collection": collection, "filename": filename, "created_at": created_at,
        #         "began_at": new_began_at, "url": current_zip_url, "state": "pending"}
    else:
        main_logger("info", "No new file on ZTM site. ")
        client.close()
        # return {}
        return False

