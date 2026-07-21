from src.site_checking.ztm_site_checker import ztm_site_checker
from src.site_checking.find_actual_schedule import find_actual_schedule
from src.site_checking.fetch_gfts_files import fetch_gtfs_files
from ztm_tools.mongo_tools.mongo_connect import create_mongo_connection
from os import getenv
from src.site_checking.calculate_checksum import calculate_checksum
from src.site_checking.mongo_entry_creator import entry_creator
from datetime import datetime, timedelta
from src.site_checking.collect_last_ztm_file import collect_last_ztm_file
from ztm_tools.logging.logger import main_logger
from bson import ObjectId

# def ztm_watcher_logic():
#     """
#     Logic of ZTM site checking. Check ZTM site
#     :return: state 1 and url when detected new file on ZTM site else 0, None
#     """
#     # 1. Check if there is new zip file
#     new_schedule_bool = ztm_site_checker()
#     # 2. Find actual url for site
#     url = find_actual_schedule()
#     if new_schedule_bool:
#         return 1, url
#     else:
#         return 0, None
def update_stop_times_archive_new(new_urls):
    """
        Update "Stop_times_archive" collection in MongoDB
        :return: none
        """
    """
    Jak to przerobić?
    Żeby mieć pewnośc, że to ten sam plik url muszę mieć jego checksum. Pobieranie wszystkich plików a następnie 
    robienie ich checksumy to raz długi czas a dwa że dużo danych.
    Pobrać 20 pierwszych plików?
    1. Pobrać listę wszystkich url z MongoDB,
    2. Pobrać listę wszystkich url ze strony ZTM,
    3. Porównać listy - jeżeli pliku nie ma w url z Mongo, od razu go dodajemy ze statusem pending,
    4. Po dodaniu dla 10 pierwszych plików sprawdzić checksumy plików pobranych z nowymi
    jeżeli dla pliku jest nowa checksuma:
        jeżeli plik ma status = "active"
        wyślij wiadomość o stat i nowe dane,
        jeżeli plik ma status "penidng":
        zaktualizuj checksume
    Potem reszta bez zmian
    Popraw błąd z dodawaniem do SQS - jak są 2 kolejki to jest jakiś error
    Jak zrobisz te 2 rzeczy to przyjmij, że micro 3 jest ready i idź do statystyki
    Sprawdź czy micro3 odczyta wiadomość i da jej printa a potem oznaczy ją jako zrobioną i przeniesie do innej kolejki
    Potem dorób statystykę
    """
    def add_file():
        print("Debug: new file, adding")
        # It doesn't exist in "Stop_times_arch" so,
        # Create new entry in collection "Stop_times_arch"
        key_for_value = [key for key, value in new_urls.items() if value == url][0]
        file, file_name = collect_last_ztm_file(new_urls[key_for_value])
        new_checksum = calculate_checksum(file)
        began_at = file_name.split("-")[0]
        entry_creator(
            collection=collection,
            new_checksum=new_checksum,
            filename=file_name,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            began_at=began_at,
            url=new_urls[key_for_value],
            state="pending"
        )

    mongo_con = create_mongo_connection(getenv("MONGO_URI"))
    collection = mongo_con["Poznan"]["Stop_times_arch"]
    need_extra_update = False
    # Create hash sum from all founded URL's
    urls_dict = {}
    print(f"Debug: starting to create checksum of all new urls. Amount of new urls: {len(list(new_urls.values()))}")
    print("Debug: check if this file exist in MongoDB")
    for url in list(new_urls.values()):
        # Check if checksum is already in our MongoDB collection "Stop_times_arch"
        examined = collection.find_one({"url": url})
        if examined:
            # If existed, we don't need to add it, so skip - continue to the next one
            examined_date = examined["began_at"]
            # print(examined_date)
            # print((datetime.now() - timedelta(days=10)).date())
            if datetime.strptime(examined_date, "%Y%m%d").date() <= (datetime.now() - timedelta(days=10)).date():
                key_for_value = [key for key, value in new_urls.items() if value == url][0]
                file, file_name = collect_last_ztm_file(new_urls[key_for_value])
                checksum = calculate_checksum(file)
                if examined["checksum"] != checksum:
                    examined["checksum"] = checksum
                    if examined["state"] == "active":
                        need_extra_update = True
                else:
                    # what if file has been changed? modify checksum, if file is active - replace and statistik!
                    continue

                print("Debug: file known, skip")
            continue
        else:
            add_file()
    mongo_con.close()
    return need_extra_update

# ----Placeholder---
def update_stop_times_archive(new_urls):
    """
    Update "Stop_times_archive" collection in MongoDB
    :return: none
    """
    mongo_con = create_mongo_connection(getenv("MONGO_URI"))
    collection = mongo_con["Poznan"]["Stop_times_arch"]
    # Create hash sum from all founded URL's
    checksum_dict = {}
    print(f"Debug: starting to create checksum of all new urls. Amount of new urls: {len(list(new_urls.keys()))}")
    # Optimalization needed! if url in mongo - skip!
    for new_date in list(new_urls.keys()):
        # Calculate checksum
        file, file_name = collect_last_ztm_file(new_urls[new_date])
        new_checksum = calculate_checksum(file)
        # Add as new entry to checksum dictionary
        checksum_dict[new_checksum] = (new_date, new_urls[new_date])
    # Check, if created hash sum exist in Stop_times_arch
    print("Debug: check if this file exist in MongoDB")
    for checksum in list(checksum_dict.keys()):
        # Check if checksum is already in our MongoDB collection "Stop_times_arch"
        if collection.find_one({"checksum": checksum}):
            # If existed, we don't need to add it, so skip - continue to the next one
            print("Debug: file known, skip")
            continue
        else:
            print("Debug: new file, adding")
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

def find_actual_active_url():
    mongo_con = create_mongo_connection(getenv("MONGO_URI"))
    collection = mongo_con["Poznan"]["Stop_times_arch"]
    return collection.find_one({"state": "active"})

def find_url_by_given_id(searched_id):
    mongo_con = create_mongo_connection(getenv("MONGO_URI"))
    collection = mongo_con["Poznan"]["Stop_times_arch"]
    searched = collection.find_one({"_id": searched_id})
    result = searched["url"]
    return result # why return = NonType?

def set_schedules_as_archival(actual_entry_id):
    """
    Set which new schedule is active and set remained to archival
    :param actual_entry_id: MongoDB document id of schedules, which stay as "active"
    :return: None, updates variable "state" for documents in MongoDB collection "Stop_times_archive"
    """
    mongo_con = create_mongo_connection(getenv("MONGO_URI"))
    collection = mongo_con["Poznan"]["Stop_times_arch"]
    all_documents = collection.find({})
    for document in all_documents:
        if document["state"] == "archival":
            continue
        if document["_id"] == actual_entry_id:
            document["state"] = "active"
            collection.update_one({"_id": document["_id"]}, {"$set": {"state": "active"}})
        else:
            if document["began_at"] > datetime.now().strftime("%Y%m%d"):
                print("Found newer schedule")
                document["state"] = "pending"
                collection.update_one({"_id": document["_id"]}, {"$set": {"state": "archival"}})
            else:
                document["state"] = "archival"
                collection.update_one({"_id": document["_id"]}, {"$set": {"state": "archival"}})
    mongo_con.close()

def check_ztm_logic():
    """
    Logic of ZTM site checking. Check ZTM site
    :return: False if there isn't new ZTM schedule, else return True
    """

    """
    TODO:
    1. Extract all schedules URLS
    2. Check which URLS are curently saved in MongoDB - add new ones
    3. Check how many files can be active for today - return them
    4. Check which one should be active for today - find this which is 
    4. If file, which should be active today has state "active" return False, else return True
    """
    # Find all schedules URLs
    print("Debug: ztm_logic_start")
    all_urs = fetch_gtfs_files()
    #  Add new files to "Stop_time_arch" collection
    extra_update = update_stop_times_archive_new(all_urs)
    print("Debug: schedules updated")
    # Find which file should be active for now
    new_actual_schedule_tuple = find_actual_schedule()
    main_logger("info", f"Today's actual schedule is for date: {new_actual_schedule_tuple[1]}")
    new_active_url = find_url_by_given_id(new_actual_schedule_tuple[0])
    # Compare actual active url with new_active - if there are the same, return False, else return True
    print("Debug: checking if we have new url")
    actual_active = find_actual_active_url()
    print(actual_active)
    print(type(actual_active))
    try:
        if extra_update:
            return True
        elif new_active_url != actual_active["url"]:
            # New actual URL - we have to update information in MongoDB collection "Stop_times_arch" and update S3!
            # Returning True will give information to program to prepare new messages
            set_schedules_as_archival(new_actual_schedule_tuple[0])
            return True
        else:
            return False
    except TypeError:
        # There is no "active" url, we need to choose one and create data
        set_schedules_as_archival(new_actual_schedule_tuple[0])
        return True

