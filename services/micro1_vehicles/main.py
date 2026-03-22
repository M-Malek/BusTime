"""
Microservice no. 1 - Vehicle time and position collector
Respond for collecting and saving in DB current vehicle position in given time period (now 30 sec.)
@M-Malek
"""
# Libs:
import time

from dotenv import load_dotenv
from src.micro_jobs import job_data_download, job_database_wipeout
from src.log_logging import main_logger
import os
from src.sqs_messages import consume

load_dotenv("config.env")


# This code has to bee adopted for AWS service. While True loop has to be replaced.
"""
def main():
    jobs = os.getenv("MICRO1_JOBS")
    current_job = os.getenv("MICRO1_CURRENT_JOB")

    # print(jobs)
    program_jobs = jobs.replace(" ", "").split(',')
    # print(new_jobs)
    # print(type(new_jobs))
    # print(current_job)
    # print(type(current_job))
    # for j in new_jobs:
    #     if str(current_job) == j:
    #         print("Jest to zadanie!")

    if len(jobs) == 0 or current_job == "":
        # print("???")
        main_logger("error", "Empty jobs list or job selector in env variables for Micro1")
        return None
    else:
        try:
            # program_jobs = list(json.load(jobs))

            if current_job in program_jobs:
                if current_job == "normal":
                    job_data_download()
                elif current_job == "wipeout":
                    job_database_wipeout()
                else:
                    main_logger("warning", "Debug: This line shouldn't been executed:"
                                           " job hasn't been selected or typed incorrectly so I run normal job")
                    job_data_download()
            else:
                print("Test")
                main_logger("error", "Given job name doesn't exist in Mirco1 jobs list!")
        except Exception as e:
            main_logger("error", f"Suprising error during executing Micro1 main.py: {e}")
"""


def main(action=True):
    """
    Main Microservice 1 action loop
    :return: default Microservice 1 workflow
    """
    while action:
        job_data_download()
        # print("Test")
        # consume()  # consume turned off - do not use micro1 to wipeout data from database!
        time.sleep(15)  # change to 15 seconds! why? one data runtime take 15 seconds


if __name__ == "__main__":
    main()
    #consume()
