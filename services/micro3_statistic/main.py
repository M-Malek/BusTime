"""
Micro3 - creating lines statistics
@M-Malek
"""

from dotenv import load_dotenv
from ztm_tools.sqs.consume.consumer import message_consumer
from src.micro_jobs import job_statistic
from datetime import datetime
from ztm_tools.s3_manager.download_data.file_downloader import download_data
from src.s3_service.s3_data_downloader import download_s3_data


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
