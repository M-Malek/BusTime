from pymongo import MongoClient
from ztm_tools.logging.logger import main_logger
from datetime import datetime

def check_jobs_status(mongo_uri):
    """
    Check micoservices searching for errors
    :return: Errors log
    """
    """
    Sprawdź status wiadomości z kolekcji status
    Sprawdź czy są jakieś wiadomości w kolekcji errors
    zwróć log ze statusem informacji na temat ilości wiadomości wykonanych i z błędem
    """
    # Connect to Mongo
    con = MongoClient(mongo_uri)
    # Check collection Events
    con_events = con["Poznan"]["Events"]
    error_in_events = con_events.find({"status": "error"})
    error_in_events_count = con_events.count_documents({"status": "error"})
    if error_in_events:
        # events_message = f"Founded {error_in_events.count_collection({})} errors"
        # events_errors_id = []
        # for event_error in error_in_events:
        #     events_errors_id.append(event_error["_id"])
        main_logger("info", f"Founded {error_in_events_count} errors")
    else:
        main_logger("info", "No errors in Events found")
        # events_message = "No errors in Events found"
    con_status = con["Poznań"]["Status"]
    error_in_status = con_status.find({"status": "error"})
    error_in_status_count = con_status.count_documents({"status": "error"})
    if error_in_status:
        # status_message = "Found {len(error_in_status)} errors"
        # status_errors_id = []
        # for status_error in error_in_status:
        #     status_errors_id.append(status_error["_id"])
        main_logger("info", f"Found {error_in_status_count} errors")
    else:
        main_logger("info", "No errors in Status found")
        # status_message = "No errors in Status found"

    con_log = con["Poznan"]["Logs"]
    total_errors = error_in_events_count + error_in_status_count
    log_message = {
        "date": datetime.now(),
        "total_errors": total_errors,
        "events_errors": error_in_events_count,
        "status_errors": error_in_status_count,
    }
    main_logger("info", f"Total errors: {total_errors}, "
                        f"statuses: {error_in_status_count}, "
                        f"events: {error_in_events_count}")
    con_log.insert_one(log_message)
    con.close()
