"""
Micro3 - creating lines statistics
@M-Malek
"""
import os
from src.vehicle_location_importer import vehicles_data_downloader
from dotenv import load_dotenv

load_dotenv("config.env")


def main():
    print("Work in progres!")
    vehicles_data_downloader()


if __name__ == "__main__":
    main()
