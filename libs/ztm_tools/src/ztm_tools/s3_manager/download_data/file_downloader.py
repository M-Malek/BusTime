import boto3
from os import getenv
from ztm_tools.logging.logger import main_logger
from pandas import read_json
from io import BytesIO

def download_data(line):
    """
    Download data for given line from S3 service
    :param line: str, number of line
    :return: data for given line or None if line not found or error
    """
    bucket = getenv('S3_BUCKET')
    storage_type = getenv('S3_STORAGE_TYPE')
    # print("S3_ENDPOINT:", getenv("S3_ENDPOINT"))
    # print("access key:", getenv("S3_ACCESS_KEY"))
    # print("secret KEY:", getenv("S3_SECRET_KEY"))
    # print("S3_ENDPOINT:", getenv("S3_ENDPOINT"))
    # print("S3_BUCKET_ENDPOINT:", getenv("S3_BUCKET_ENDPOINT"))
    if storage_type == "minio":
        s3 = boto3.client(
            "s3",
            endpoint_url=getenv("S3_BUCKET_ENDPOINT"),
            aws_access_key_id=getenv("S3_ACCESS_KEY"),
            aws_secret_access_key=getenv("S3_SECRET_KEY")
        )
        #print(s3.list_buckets())
    elif storage_type == "aws":
        s3 = boto3.client("s3")
    else:
        main_logger('error', "Download S3 data error: no given storage type")
    # print("bucket:", repr(bucket))
    # print("line:", repr(line))
    # print("line type:", type(line))
    response = s3.get_object(
        Bucket=bucket,
        Key=f"stop_times/line-{line}.json"
    )
    return read_json(BytesIO(response['Body'].read()))
