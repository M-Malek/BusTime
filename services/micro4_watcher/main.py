from dotenv import load_dotenv
from logic.stoptime_watcher_logic import ztm_watcher_logic
from ztm_tools.sqs.accomplish_work import accomplish_all_works
from ztm_tools.sqs.error_message_handler import error_message_handler
from ztm_tools.sqs.check_jobs_status import check_jobs_status
from src.s3_checking.checker import s3_checker
from src.s3_messaging.create_message_statistic import create_message_statistic
from src.s3_messaging.create_message_schedules import create_message_schedules
import asyncio
from ztm_tools.mongo_tools.check_message_accomplished import check_message_accomplished
from ztm_tools.mongo_tools.mongo_connect import create_mongo_connection
import os

load_dotenv("config.env")


def main():
    while True:
        # 1. Check microservices status from status SQS
        check_jobs_status(os.getenv("MONGO_URI"))
        # 2. Handle catch errors
        error_message_handler()
        # 3. Check ZTM site and check if S3 has data
        # 3.1 S3 empty:
        empty_s3 = False
        if s3_checker():
            # 3.1.1 Send message to download new data
            # 3.1.2 Wait for message with succeed, then log task accomplished
            empty_s3 = True
            new_schedules_id = asyncio.create_task(create_message_schedules())
        # 4. If new .zip file detected:
        # CHECK LOGIC FROM HERE
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

        # 4.1.1 should be active now:
        # 4.1.1.1 Send message to generate statistic
        # 4.1.1.2 Wait for message with succeed, then log task accomplished
        # 4.1.1.3 Send message to download new data
        # 4.1.1.4 Wait for message with succeed, then log task accomplished
        # 4.2.1 Shouldn't be active
        # 4.2.2 Send message to generate statistic
        # 4.2.3 Wait for message with succeed, then log task accomplished

        pass

if __name__ == "__main__":
    main()

