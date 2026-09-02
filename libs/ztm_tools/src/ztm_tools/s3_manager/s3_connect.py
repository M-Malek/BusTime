from boto3 import client
from os import getenv
from ztm_tools.logging.logger import main_logger
from time import sleep

def s3_connect():
    attempts = 3
    while attempts < 3:
        try:
            s3 = client(
                "s3",
                endpoint_url=getenv("S3_ENDPOINT"),
                aws_access_key_id=getenv("S3_ACCESS_KEY"),
                aws_secret_access_key=getenv("S3_SECRET_KEY"),
            )
            return s3
        except Exception as e:
            main_logger("error", f"Cannot connect to S3, error: {e}")
        attempts -= 1
        sleep(15)
    main_logger("error", "Cannot connect to S3")
    return None
