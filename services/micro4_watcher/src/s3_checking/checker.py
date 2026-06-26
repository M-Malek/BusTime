from botocore.exceptions import EndpointConnectionError, ClientError
from trash.log_logging import main_logger
import os


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
        response = client.list_objects_v2(
            Bucket=os.getenv("S3_BUCKET"))
        if "Contents" in response:
            # print("S3 has data!")
            return False
        else:
            # print("S3 is empty!")
            return True

        # return False if "Contents" in response else True

    except EndpointConnectionError:
        main_logger("error", "Endpoint Connection Error!")
        return False
    except ClientError as e:
        main_logger("error", f"Cannot check S3 status! Error: {e}")
        return False
