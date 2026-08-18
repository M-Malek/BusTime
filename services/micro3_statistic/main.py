"""
Micro3 - creating lines statistics
@M-Malek
"""
import os
from src.vehicle_location_importer import vehicles_data_downloader
from dotenv import load_dotenv
from ztm_tools.sqs.consume_old import test
from src.message_checker import check_messages
from ztm_tools.sqs.receive_messages import receive_all_messages, get_all_messages
from ztm_tools.sqs.consume.consumer import message_consumer


load_dotenv("config.env")

# GLOBAL VARIABLES
FUNCTION_MAP = {
    "statistic": print,
}


def main():
    print("Work in progres!")
    # check_messages(FUNCTION_MAP)
    # recived_messages = receive_all_messages("m3")
    # print(recived_messages)
    message_consumer("m3", "events", FUNCTION_MAP)

if __name__ == "__main__":
    main()
