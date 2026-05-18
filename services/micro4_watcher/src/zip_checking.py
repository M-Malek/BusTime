from src.site_checking.ztm_site_checker import checksum_checker
from src.s3_checking.checker import s3_checker
from boto3 import client
import os
from botocore.config import Config
from src.log_logging import main_logger


def status_describer():
    """
    Describe status for job_normal:
    - if there is new file on ZTM server and S3 is empty - download new data - return status 1
    - if there is empty S3 - download new data - return status 2
    - if there is new file on ZTM server and S3 isn't empty - empty S3 and download new data - return status 3
    - if there isn't new file on ZTM server - skip - return status 4
    """
    checksum_bool = checksum_checker()
    print(f"Debug in status_describer: checksum_bool: {checksum_bool}")
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
        # print(s3.meta.endpoint_url)
    except Exception as e:
        main_logger("error", "Cannot check s3 and checksum to define an action")
        return 5
    # s3_bool = s3_checker(s3)
    s3_bool = True
    if checksum_bool and s3_bool:
        return 1
    elif s3_bool:
        return 2
    elif checksum_bool and not s3_bool:
        return 3
    elif checksum_bool:
        return 4
    else:
        return None
