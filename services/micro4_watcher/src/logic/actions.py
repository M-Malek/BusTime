from src.logic.status_describer import get_status
from src.job_messages import message_get_stops, message_get_statistic, message_get_stoptimes
from src.log_logging import main_logger
from src.sqs_messages import send_event


async def check_ztm():
    # print("Debug: check_ztm is running!")
    status = get_status()
    # print(f"Debug: status number: {status}")
    match status:
        # REWORK NEEDED!!!
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