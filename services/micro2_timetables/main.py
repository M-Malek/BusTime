"""
Main.py file for Microservice 2 - parsing data tables from ZTM server
@M-Malek
"""

# For debug - moving micro2 to own env
import os
from dotenv import load_dotenv

#Libs:
import json
from src.log_logging import main_logger
from src.micro_jobs import job_stops, job_normal, job_shapes

load_dotenv("config.env")


def main(action_type="normal"):
    jobs = os.getenv("MICRO2_JOBS")
    current_job = os.getenv("MICRO2_CURRENT_JOB")

    if jobs or current_job is None:
        main_logger("error", "Empty jobs list or job selector in env variables for Micro2")
        return None
    else:
        try:
            program_jobs = json.load(jobs)

            if current_job in program_jobs:
                if current_job == "normal":
                    job_normal()
                elif current_job == "shapes":
                    job_shapes()
                elif current_job == "stops":
                    job_stops()
                else:
                    main_logger("warning", "Debug: This line shouldn't been executed:"
                                           " job hasn't been selected so I run normal job")
                    job_normal()
            else:
                main_logger("error", "Given job name doesn't exist in Mirco2 jobs list!")
        except Exception as e:
            main_logger("error", f"Suprising error during executing Micro2 main.py: {e}")


if __name__ == "__main__":
    main()
