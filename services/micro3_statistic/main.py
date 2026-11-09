"""
Micro3 - creating lines statistics
@M-Malek
"""

from dotenv import load_dotenv
from src.micro_jobs import job_statistic


load_dotenv("config.env")


FUNCTION_MAP = {
    "statistic": job_statistic,
}


def main():
    #message_consumer('m3', 'events', FUNCTION_MAP)
    #data = download_s3_data("1")
    job_statistic()

if __name__ == "__main__":
    main()
