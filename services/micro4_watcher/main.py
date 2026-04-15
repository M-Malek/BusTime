from dotenv import load_dotenv
import os
from src.job_messages import message_get_stops, message_get_statistic, message_get_stoptimes
from src.zip_checking import status_describer


load_dotenv("config.env")


def main():
    # Only for first program run:
    # message_get_stops()
    # Step 1: check ztm_site: check if there is new file on ZTM server
    status = status_describer()
    match status:
        case 1 | 2:
            #  Download new data
            pass
        case 3:
            # Download new data, run statistic
            pass
        case 4:
            pass
        case _:
            pass
    # Step 2: check time: if time in time_list_period, send message to SQS for statistic


if __name__ == "__main__":
    main()
