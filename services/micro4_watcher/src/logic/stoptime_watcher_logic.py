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
from ztm_tools.sorting.dates_sorting import data_range_sorter
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
def update_stop_times_archive(new_urls):
    """
        Update "Stop_times_archive" collection in MongoDB
        :return: none
        """

    def add_file():
        #print("Debug: new file, adding")
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
    # cooldown_counter - variable to cut amount of files checked by function. It should cut program runtime time
    cooldown_counter = 10
    for url in list(new_urls.values()):
        #print(f"Debug: {cooldown_counter}")
        if cooldown_counter == 0:
            break
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
                    # what if file has been changed? modify checksum, if file is active - replace and statistic!
                    examined["checksum"] = checksum
                    if examined["state"] == "active":
                        need_extra_update = True
                else:
                    cooldown_counter -= 1
                    continue

                #print("Debug: file known, skip")
            cooldown_counter -= 1
            continue
        else:
            add_file()
            cooldown_counter -= 1
    mongo_con.close()
    return need_extra_update


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

def organize_documents_state(actual_entry_id=None):
    """
    Organize dates 'began_at' MongoDB documents from Stop_times_arch collection.
    Set 'active' document, 'pending' documents and 'archival' documents
    :param actual_entry_id: MongoDB document id of schedules, which stay as "active"
    :return: None, updates variable "state" for documents in MongoDB collection "Stop_times_archive"
    """
    mongo_con = create_mongo_connection(getenv("MONGO_URI"))
    collection = mongo_con["Poznan"]["Stop_times_arch"]
    db = mongo_con["Poznan"]
    # print(db.list_collection_names())
    # print("Collection:", collection.name)
    # print("Count", collection.count_documents({}))
    all_documents = collection.find({})
    if actual_entry_id is None:
        # There is no 'active' document, we need to find document which should be now active
        # Prepare data for data_range_sorter:
        prepared_documents = []
        for document in all_documents:
            # print(document['_id'])
            prepared_documents.append((document["_id"], document["file_name"]))
        # Find proper entry (entry which should be now active)
        actual_active = data_range_sorter(datetime.strftime(datetime.now(), "%Y%m%d"), prepared_documents)
        # Update entry in collection to set it as active
        collection.update_one({"_id": actual_active[0]}, {"$set": {"state": "active"}})
    for document in all_documents:
        # if document["state"] == "archival":
        #     continue
        if document["_id"] == actual_entry_id:
            document["state"] = "active"
            collection.update_one({"_id": document["_id"]}, {"$set": {"state": "active"}})
        else:
            active = collection.find_one({"state": 'active'})
            # newer_as_active - bool: True if examined document has 'began_at' date greater than document
            # with status 'active'
            newer_as_active = (datetime.strptime(document["began_at"], "%Y%m%d") >
                               datetime.strptime(active['began_at'], "%Y%m%d"))
            #print(f"Debug: newer_as_active: {newer_as_active}: {document['file_name']}")
            #if document["began_at"] > datetime.now().strftime("%Y%m%d"):
            if newer_as_active:
                # print("Found newer schedule")
                document["state"] = "pending"
                collection.update_one({"_id": document["_id"]}, {"$set": {"state": "pending"}})
            else:
                document["state"] = "archival"
                collection.update_one({"_id": document["_id"]}, {"$set": {"state": "archival"}})
    mongo_con.close()

def create_new_actual(id_to_set_as_active):
    """
    Create entry with state 'active' if this state doesn't exist in 'Stop_times_arch' collection
    For this case, take entry from function find_actual_schedule() as actual
    :return: Nothing, creates entry with state 'active' in Mongo DB collection 'Stop_times_arch'
    """
    #Establish connection and choose collection 'Stop_times_arch'
    #print("create_new_actual start working!")
    mongo_con = create_mongo_connection(getenv("MONGO_URI"))
    collection = mongo_con["Poznan"]["Stop_times_arch"]
    # Check once more, it there isn't entry with state 'active'
    active = collection.find_one({"state": "active"})
    #print(f"Debug: active: {active}")
    if active is None:
        # Find entry with _id from find_actual_schedule() result
        #print(f"Debug: id: {id_to_set_as_active}")
        new_active = collection.find_one({"_id": id_to_set_as_active})
        #print(f"Debug: new_active: {new_active}")
        if new_active is not None:
            collection.update_one({"_id": id_to_set_as_active}, {"$set": {"state": "active"}})
        # If error with finding _id, take first entry from 'Stop_times_arch'
        else:
            document = collection.find_one(
                sort=[("created_at", -1)]
            )
            #print(f"Debug: document: {document}")
            # Set founded _id parameter state as 'active'
            if document:
                collection.update_one(
                    {"_id": document["_id"]},
                    {"$set": {"state": "active"}}
                )

def check_ztm_logic():
    """
    Logic of ZTM site checking. Check ZTM site
    Function logic:
    1. Extract all schedules URLS
    2. Check which URLS are curently saved in MongoDB - add new ones
    3. Check how many files can be active for today - return them
    4. Check which one should be active for today - find this which is
    4. If file, which should be active today has state "active" return False, else return True
    :return: False if there isn't new ZTM schedule and updating S3 storage is unnecessary, else return True
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
    all_urs = fetch_gtfs_files()
    #  Add new files to "Stop_time_arch" collection
    extra_update = update_stop_times_archive(all_urs)
    # Find which file should be active for now
    new_actual_schedule_tuple = find_actual_schedule()
    main_logger("info", f"Today's actual schedule is for date: {new_actual_schedule_tuple[1]}")
    new_active_url = find_url_by_given_id(new_actual_schedule_tuple[0])
    # Compare actual active url with new_active - if there are the same, return False, else return True
    actual_active = find_actual_active_url()
    #print(f"Type of new_active_url: {type(new_active_url)}")
    #print(f"Type of actual_active: {type(actual_active)}")
    if actual_active is None:
        create_new_actual(new_actual_schedule_tuple[0])
    try:
        #print(f"Debug: new_active_url != actual_active['url']: {new_active_url != actual_active['url']}")
        if extra_update:
            return True
        elif new_active_url != actual_active["url"]:
            # New actual URL - we have to update information in MongoDB collection "Stop_times_arch" and update S3!
            # Returning True will give information to program to prepare new messages
            organize_documents_state(new_actual_schedule_tuple[0])
            return True
        else:
            return False
    except TypeError:
        # There is no "active" url, we need to choose one and create data
        organize_documents_state(new_actual_schedule_tuple[0])
        return True

