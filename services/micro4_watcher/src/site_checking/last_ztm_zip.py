from datetime import datetime, date
from site_checking.fetch_gfts_files import fetch_gtfs_files

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
        return None
