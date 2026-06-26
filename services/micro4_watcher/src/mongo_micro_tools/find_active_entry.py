from ztm_tools.mongo_tools.mongo_connect import create_mongo_connection
from ztm_tools.mongo_tools.check_pending_state import check_pending_state
from src.site_checking.find_actual_schedule import find_actual_schedule
import os

def find_active_entry():
    """
    Find active entry
    :return:
    """
    # 2. Check which MongoDB documents has state "pending" - save theirs id in pending_docs list
    con = create_mongo_connection(os.getenv("MONGO_URI"))
    coll = con["Poznan"]["Stop_times_arch"]
    pending_docs = check_pending_state(coll)
    # 3. Check which MongoDB documents should be active for today - id of entry save as today_actual variable
    today_actual_id = find_actual_schedule()
    # 4. Set current active schedule as "archival"
    actual_schedule= coll.find_one({"state": "actual"})
    actual_schedule.state = "archival"
    # 4. Set state of today_actual as active
    todays_schedule = coll.find_one({"_id": today_actual_id})
    todays_schedule.state = "active"
    # 5. Set state of pending_docs without today_actual as historical? Why? You can have newer entry for
    # future schedules
    # pending_docs.remove(today_actual_id)
    # for ids in pending_docs:
    #     changed_doc = coll.find_one({"_id": ids})
    #     changed_doc.state = "archival"
    con.close()
    return todays_schedule.url