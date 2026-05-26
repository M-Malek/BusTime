"""
Micro3 - creating lines statistics
@M-Malek
"""
import os
from src.vehicle_location_importer import vehicles_data_downloader
from dotenv import load_dotenv
from ztm_tools.sqs.consume import test


load_dotenv("config.env")

# GLOBAL VARIABLES
FUNCTION_MAP = {
    "statistic": print,
    
}


def main():
    print("Work in progres!")
    test()
    # vehicles_data_downloader()


if __name__ == "__main__":
    main()
