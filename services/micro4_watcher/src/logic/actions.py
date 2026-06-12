from src.logic.status_describer import get_status
from src.job_messages import message_get_stops, message_get_statistic, message_get_stoptimes
from src.log_logging import main_logger
from src.sqs_messages import send_event
from ztm_tools.logging import logger


async def check_ztm():
    # print("Debug: check_ztm is running!")
    status = get_status()
    # print(f"Debug: status number: {status}")
    match status:
        # REWORK DONE - needed again because logic problem found
        case 1:
            # Case 1: new file on ZTM site and S3 is empty - program needs new data of stoptimes
            # Case 2: S3 is empty - program needs data of stoptimes for statistic
            #  Download new data
            msg = message_get_stoptimes()
            # print(f"Debug in check_ztm: msg: {msg}")
            send_event(msg)
            main_logger("info", "New data on ZTM site: "
                                "SQS message send: Download new stop times data")
        case 2:
            # Case 2: S3 is empty - program needs data of stoptimes for statistic
            #  Download new data
            msg = message_get_stoptimes()
            # print(f"Debug in check_ztm: msg: {msg}")
            send_event(msg)
            main_logger("info", "Detected empty S3: "
                                "SQS message send: Download new stop times data")
        case 3:
            # Download new data, run statistic
            msg_stat = message_get_statistic()
            print(f"Debug in check_ztm: msg_stat: {msg_stat}")
            send_event(msg_stat)
            msg_data = message_get_stoptimes()
            print(f"Debug in check_ztm: msg_data: {msg_data}")
            send_event(msg_data)
            main_logger("info", "New data on ZTM site: SQS messages send: "
                                "Download new stop times data, make statistic")
        case 4:
            main_logger("info", "ZTM site hasn't changed!")
        case 5:
            main_logger("error", "Microservice 4 cannot identify, "
                                 "which data needs to be changed/update.")
        case _:
            pass

async def run_statistic():
    msg_stat = message_get_statistic()
    print(f"Debug in run_statistic: msg_stat: {msg_stat}")
    send_event(msg_stat)
    main_logger("info", "Automatic SQS message for statistic send!")

async def check_stops_collection():
    pass

def ztm_site_checker():
    """
    Main function
    :return: None
    """
    """
    
    
    """
    from src.logic.stoptime_watcher_logic import ztm_watcher_logic
    # 1. Check if S3 bucket ztm_poznan is empty
    # 2. Check ztm_site
    print(ztm_watcher_logic)
    if ztm_watcher_logic == "data and statistic":
        # Send message to statistic
        # Send message to download new data to S3
        msg_stat = message_get_statistic()
        send_event(msg_stat)
        main_logger("info", "Sending statistic")
        # Add to SQS message url to actual data!
        msg_stop_times = message_get_stoptimes()
        send_event(msg_stop_times)
        main_logger("info", "Sending new datatime")

    elif ztm_watcher_logic == "statistic":
        # Send message to statistic
        msg_stat = message_get_statistic()
        send_event(msg_stat)
        main_logger("info", "Sending statistic")

    elif ztm_watcher_logic == "No new data":
        # Don't do anything
        logger("info", "No new data detected")