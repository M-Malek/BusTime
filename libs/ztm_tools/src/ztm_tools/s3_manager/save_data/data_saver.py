from boto3 import client
from os import getenv
from ztm_tools.logging.logger import main_logger
from ztm_tools.s3_manager.s3_connect import s3_connect
from json import dumps

def save_data_in_bucket(s3, bucket_name, bucket_prefix, file_name, data):
    """
    Save data to S3 bucket in S3
    :param s3: S3 object
    :param bucket_name: str, bucket_name
    :param bucket_prefix: str, bucket_prefix
    :param file_name: str, file_name
    :param data: data to save
    :return: None
    """

    #bucket_name = getenv("S3_BUCKET")
    #bucket_prefix = "shapes"

    # utworzenie bucket (jeśli nie istnieje)
    try:
        s3.create_bucket(Bucket=bucket_name)
    except Exception as e:
        # main_logger("error", "micro_jobs.py: S3 bucket has been created earlier")
        pass

    connection_counter = 1  # counter of connection attempts to save file in S3
    # bucket_prefix = getenv("S3_BUCKET_PREFIX")
    while connection_counter <= 4:
        try:
            file_key = f"{bucket_prefix}/{file_name}.json"
            s3.put_object(
                Bucket=getenv("S3_BUCKET"),
                Key=file_key,
                Body=dumps(data, ensure_ascii=False).encode("utf-8"),
                ContentType="application/json"
            )
            return str(file_name)
        except Exception as e:
            main_logger("warning", f"Attempt {connection_counter} to save data with name "
                                   f"{bucket_prefix}-{file_name} failed \n"
                                   f"Reattempting: error: {e}")
            connection_counter += 1

    if connection_counter > 4:
        main_logger("error", f"Saving data in {bucket_prefix}-{file_name} failed")
        return ""
    else:
        main_logger("error", "Undiscovered error in save_data_in_bucket. Saving failed")
        return None