"""
Main.py file for Microservice 2 - parsing data tables from ZTM server
@M-Malek
"""

# For debug - moving micro2 to own env
import os
from dotenv import load_dotenv
# from src.sqs_messages import consume
from ztm_tools.sqs.consume.consumer import message_consumer

#Libs:
import json
from src.log_logging import main_logger
from src.micro_jobs import job_stops, job_shapes, job_schedules, job_empty

load_dotenv("config.env")


# def main():
#     jobs = os.getenv("MICRO2_JOBS")
#     current_job = os.getenv("MICRO2_CURRENT_JOB")
#
#     # print(jobs)
#     program_jobs = jobs.replace(" ", "").split(',')
#     # print(new_jobs)
#     # print(type(new_jobs))
#     # print(current_job)
#     # print(type(current_job))
#     # for j in new_jobs:
#     #     if str(current_job) == j:
#     #         print("Jest to zadanie!")
#
#     if len(jobs) == 0 or current_job == "":
#         # print("???")
#         main_logger("error", "Empty jobs list or job selector in env variables for Micro2")
#         return None
#     else:
#         try:
#             # program_jobs = list(json.load(jobs))
#
#             if current_job in program_jobs:
#                 if current_job == "normal":
#                     job_normal()
#                 elif current_job == "shapes":
#                     job_shapes()
#                 elif current_job == "stops":
#                     job_stops()
#                 else:
#                     main_logger("warning", "Debug: This line shouldn't been executed:"
#                                            " job hasn't been selected or typed incorrectly so I run normal job")
#                     job_normal()
#             else:
#                 main_logger("error", "Given job name doesn't exist in Mirco2 jobs list!")
#         except Exception as e:
#             main_logger("error", f"Suprising error during executing Micro2 main.py: {e}")

FUNCTION_MAP = {
    "schedules": job_schedules,
    "stops": job_stops,
    "shapes": job_shapes,
    "empty": job_empty,
}

def main():
    # message_consumer("m2", "Events", FUNCTION_MAP)
    job_stops("https://www.ztm.poznan.pl/pl/dla-deweloperow/getGTFSFile/?file=20260829_20260920.zip")

if __name__ == "__main__":
    main()
    # consume()
