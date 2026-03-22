from dotenv import load_dotenv
import os
from src.job_messages import message_get_stops, message_get_statistic, message_get_stoptimes


load_dotenv("config.env")


def main():
    # Only for first program run:
    message_get_stops()


if __name__ == "__main__":
    main()
