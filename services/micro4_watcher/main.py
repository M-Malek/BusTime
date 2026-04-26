import asyncio
from datetime import datetime
from dotenv import load_dotenv
import os
from src.job_messages import message_get_stops, message_get_statistic, message_get_stoptimes
from src.zip_checking import status_describer
from src.sqs_messages import send_event
from src.job_messages import message_get_stops, message_get_statistic, message_get_stoptimes
from src.log_logging import main_logger


load_dotenv("config.env")


async def check_ztm():
    status = status_describer()
    match status:
        case 1 | 2:
            #  Download new data
            msg = message_get_stoptimes()
            send_event(msg)
            main_logger("info", "New data on ZTM site: SQS message send: Download new stop times data")
        case 3:
            # Download new data, run statistic
            msg_stat = message_get_statistic()
            send_event(msg_stat)
            msg_data = message_get_stoptimes()
            send_event(msg_data)
            main_logger("info", "New data on ZTM site: SQS messages send: Download new stop times data, make statistic")
        case 4:
            main_logger("info", "ZTM site hasn't changed!")
        case _:
            pass


async def run_statistic():
    msg_stat = message_get_statistic()
    send_event(msg_stat)
    main_logger("info", "Automatic SQS message for statistic send!")


def main():
    # Only for first program run:
    # message_get_stops()
    last_run = set()
    statistic_hours_times = os.getenv("STAT_HOURS_TIME")
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        stat_time_list = [datetime.time(hour=h) for h in os.getenv("STAT_HOURS_TIME")]
        ztm_time_list = [datetime.time(hour=h) for h in list(range(1, 24))]
        # Step 1: check ztm_site: check if there is new file on ZTM server
        if now in ztm_time_list:
            await check_ztm()
        # Step 2: check time: if time in time_list_period, send message to SQS for statistic
        if now in stat_time_list:
            await run_statistic()


if __name__ == "__main__":
    main()
