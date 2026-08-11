from botocore.exceptions import ClientError

from dotenv import load_dotenv
from src.logic.stoptime_watcher_logic import check_ztm_logic
# from src.logic.stoptime_watcher_logic import ztm_watcher_logic,
from ztm_tools.sqs.accomplish_work import accomplish_all_works
from ztm_tools.sqs.error_message_handler import error_message_handler
from ztm_tools.sqs.check_jobs_status import check_jobs_status
from src.s3_checking.checker import s3_checker
from src.s3_checking.s3_connect import s3_connect
from src.s3_messaging.create_message_statistic import create_message_statistic
from src.s3_messaging.create_message_schedules import create_message_schedules
import asyncio
from ztm_tools.mongo_tools.check_message_accomplished import check_message_accomplished
from ztm_tools.mongo_tools.mongo_connect import create_mongo_connection
from ztm_tools.logging.logger import main_logger
import os
import time

load_dotenv("config.env")


def main_check_ztm_loop():
    """
    Main loop to checking files with schedules on ZTM site.
    :return:
    """
    print("Debug: checking S3")
    s3_status = s3_checker(s3_connect())
    if s3_status:
        # 3.1.1 Send message to download new data
        # 3.1.2 Wait for message with succeed, then log task accomplished
        # empty_s3 = True
        # new_schedules_id = asyncio.create_task(create_message_schedules())
        create_message_schedules()
        print("Debug: no S3, created message schedules")
    elif s3_status == "EndPoint Connection Error!":
        # Add case when S3 is unavailable!
        main_logger("error", "Cannot connect to S3 - check S3 status!")
    elif type(s3_status) == ClientError:
        main_logger("error", f"S3 bucket ztm_poznan master error: {s3_status}")
    else:
        # 4. If new .zip file detected:
        print("Debug: checking ztm")
        # 4.1 Check ztm logic to determinate, if we need to update S3 bucket
        if check_ztm_logic():
            print("Debug: new schedules on ZTM site")
            # check_ztm_logic = True
            # We have new entry with new schedules data for today
            # or entry with schedules for today has been modified
            # We need to create statistic and update data
            # Create message for statistic
            print("Debug: sending message statistic!")
            create_message_statistic()
            # Create message for a new data
            print("Debug: sending message schedules!")
            create_message_schedules()
        else:
            print("Debug: no new schedules on ZTM site")
            # check_ztm_logic = False
            # We don't have any new schedules, so create normal statistic
            create_message_statistic()

def main():
    while True:
        # 1. Check microservices status from status SQS
        check_jobs_status(os.getenv("MONGO_URI"))
        # 2. Handle catch errors
        error_message_handler()
        # 3. Check ZTM site and check if S3 has data
        main_check_ztm_loop()

        # Only for tests:
        print("Debug: going to sleep")
        time.sleep(120)
        # FUNCTION READY FOR MAIN TEST
        """
        !!!!tutaj!!!!!
        Postaw Elastic na 2 kolejki,
        Potem wyczyść MongoDB,
        Potem testuj!
        Updater schedules (micro 2) sprawdza przy każdym uruchomieniu, czy nie ma komendy czekaj
        Jak ma komendę czekaj to znaczy że statystyka pracuje, wtedy pozostaje w pętli sprawdzając co minutę,
        czy czasem statystyka nie skończyła. Jak statystyka skończy to dopiero wtedy pobiera dane
        zip_status, url = ztm_watcher_logic()
        if zip_status:
            # 4.1 Check if it should be active now:
            # Check which one is active now, check if it should still be active
            if empty_s3:
                con = create_mongo_connection(os.getenv("MONGO_URI"))
                logs_con = con["Poznan"]["status"]
                if check_message_accomplished(new_schedules_id):
                    stat_task_id = asyncio.create_task(create_message_statistic())
                else:
                    stat_task_id = asyncio.create_task(create_message_statistic())
                    schedules_task_id = asyncio.create_task(create_message_schedules())
        # Add code to check all messages to Microservice 3

        # 4.1.1 should be active now:
        # 4.1.1.1 Send message to generate statistic
        # 4.1.1.2 Wait for message with succeed, then log task accomplished
        # 4.1.1.3 Send message to download new data
        # 4.1.1.4 Wait for message with succeed, then log task accomplished
        # 4.2.1 Shouldn't be active
        # 4.2.2 Send message to generate statistic
        # 4.2.3 Wait for message with succeed, then log task accomplished

        pass
        """

if __name__ == "__main__":
    main()

