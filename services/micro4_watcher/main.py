import time
import os
import asyncio
from dotenv import load_dotenv
from src.logic.actions import check_ztm, run_statistic


load_dotenv("config.env")


async def main():
    # Only for first program run:
    # message_get_stops()
    last_run = set()
    statistic_hours_times = os.getenv("STAT_HOURS_TIME")
    while True:
        """
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
        """

        # Debug:
        await check_ztm()
        # await run_statistic()
        time.sleep(15)


if __name__ == "__main__":
    asyncio.run(main())
