"""Clent creator for ZTM Tools"""
from boto3 import client
from botocore.config import Config
from ztm_tools.logging.logger import main_logger
import os

def s3_connect():
    try:
        config = Config(
            connect_timeout=3,
            read_timeout=5,
            retries={'max_attempts': 3}
        )
        s3 = client(
            "s3",
            endpoint_url=os.getenv("S3_BUCKET_ENDPOINT"),
            aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("S3_SECRET_KEY"),
            config=config
        )
        #print(s3.meta.endpoint_url)
        #a= input("Debug: Do you want to test connection with S3? (y/n): ")
        return s3
    except Exception as e:
        main_logger("error", "Cannot check s3 and checksum to define an action")
        return None
