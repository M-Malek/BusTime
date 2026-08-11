from ztm_tools.mongo_tools.mongo_connect import create_mongo_connection
from os import getenv
from src.site_checking.calculate_checksum import calculate_checksum
from src.site_checking.mongo_entry_creator import entry_creator
from datetime import datetime, timedelta
from src.site_checking.collect_last_ztm_file import collect_last_ztm_file

def update_stop_times_archive(new_urls):
    """
    Update "Stop_times_archive" collection in MongoDB
    :return: none
    """
    mongo_con = create_mongo_connection(getenv("MONGO_URI"))
    collection = mongo_con["Poznan"]["Stop_times_arch"]
    # Create hash sum from all founded URL's
    checksum_dict = {}
    # print(f"Debug: starting to create checksum of all new urls. Amount of new urls: {len(list(new_urls.keys()))}")
    # Optimization needed! if url in mongo - skip!
    for new_date in list(new_urls.keys()):
        # Calculate checksum
        file, file_name = collect_last_ztm_file(new_urls[new_date])
        new_checksum = calculate_checksum(file)
        # Add as new entry to checksum dictionary
        checksum_dict[new_checksum] = (new_date, new_urls[new_date])
    # Check, if created hash sum exist in Stop_times_arch
    for checksum in list(checksum_dict.keys()):
        # Check if checksum is already in our MongoDB collection "Stop_times_arch"
        if collection.find_one({"checksum": checksum}):
            # If existed, we don't need to add it, so skip - continue to the next one
            continue
        else:
            # It doesn't exist in "Stop_times_arch" so,
            # Create new entry in collection "Stop_times_arch"
            began_at = checksum_dict[checksum][0].split("_")[0]
            entry_creator(
                collection=collection,
                new_checksum=checksum,
                filename=checksum_dict[checksum][0],
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                began_at=began_at,
                url=checksum_dict[checksum][1],
                state="pending"
            )
    mongo_con.close()