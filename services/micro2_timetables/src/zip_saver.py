"""
Save data prepared by microservice 2 in DynamoDB
@M-Malek
"""
# import boto3
import json
import os

import boto3
from botocore.exceptions import EndpointConnectionError, ClientError

from src.log_logging import main_logger


# from shared.tools.env_os_variables import aws_zip_bucket_name, aws_zip_object_key


def s3_checker(client):
    """
    Check, if:
    - there is connection with S3
    - S3 has data container with line's data

    :return: True if connection and empty data container - new data should be downloaded else False
    """
    # s3 = boto3.client("s3")
    # Błąd logiczny! Ten kod uruchamia się zawsze
    # response = s3.list_objects_v2(Bucket=os.getenv("S3_BUCKET"))
    try:
        response = client.list_objects_v2(Bucket=os.getenv("S3_BUCKET"))
        if "Contents" in response:
            print("S3 has data!")
            return False
        else:
            print("S3 is empty!")
            return True

        # return False if "Contents" in response else True

    except EndpointConnectionError:
        return False
    except ClientError as e:
        mian_logger("error", f"Cannot check S3 status! Error: {e}")
        return False


# def save_zip_data(client, data):
#     """
#     Save data extracted from .zip file in Amazon Web Services
#     :param client: AWS Boto3 Client
#     :param data: data to save in bucket
#     :return: saving data in bucket or error
#     """
#     try:
#         """client.put_object(
#             Bucket=aws_zip_bucket_name,
#             Key=aws_zip_object_key,
#             Body=json.dumps(data, ensure_ascii=False),
#             ContentType="application/json"
#         )"""
#         client.put_object(
#             Bucket=os.getenv("S3_BUCKET"),
#             Key=os.getenv("S3_ACCESS_KEY"),
#             Body=json.dumps(data, ensure_ascii=False),
#             ContentType="application/json"
#         )
#         main_logger("info", "ZIP data saved in AWS Bucket~!")
#     except Exception as e:
#         main_logger("error", f"Error during saving .zip data to AWS Bucket: {e}")

def single_data_saver_with_retry(client, single_data, line_number):
    """
    Save one portion of data with retry if errors with saving occures
    :param client: S3 client connection object
    :param data: one portion of data from ztm data
    :return:
    """
    connection_counter = 1  # counter of connection attempts to save file in S3
    bucket_prefix = os.getenv("S3_BUCKET_PREFIX")
    while connection_counter <= 4:
        try:
            file_key = f"{bucket_prefix}{line_number}.json"
            client.put_object(
                Bucket=os.getenv("S3_BUCKET"),
                Key=file_key,
                Body=json.dumps(single_data, ensure_ascii=False).encode("utf-8"),
                ContentType="application/json"
            )
            return str(line_number)
        except Exception as e:
            main_logger("warning", f"Attempt {connection_counter} to save data of line {line_number} failed"
                                   f"Reattempting")
            connection_counter += 1
    if connection_counter > 4:
        main_logger("error", f"Saving line {line_number} failed")
        return ""


def save_data(client, data):
    # import json
    # with open("json_stops.json", "w") as file:
    #     json.dump(stoptimes_data, file)
    #     file.close()
    """
    Save stop times data in S3 bucket
    :param client: S3 connection client
    :param data: dict, data collected and serialized from ZTM server,
    :return:
    """

    bucket_name = os.getenv("S3_BUCKET")
    bucket_prefix = os.getenv("S3_BUCKET_PREFIX")
    saved_lines = ""
    print("Debug: starting to save data!")
    for line, line_data in data.items():
        saved_line_number = single_data_saver_with_retry(client, line_data, line)
        saved_lines += saved_line_number + ", "
        # file_key = f"{bucket_prefix}{line}.json"
        # try:
        #     client.put_object(
        #         Bucket=os.getenv("S3_BUCKET"),
        #         Key=file_key,
        #         Body=json.dumps(line_data, ensure_ascii=False).encode("utf-8"),
        #         ContentType="application/json"
        #     )
        # except Exception as e:
        #     main_logger("warning", f"Micro2 job_normal: failed to save line: {line}, error: {e}")
    main_logger("info", f"Saved data of lines: {saved_lines}")
