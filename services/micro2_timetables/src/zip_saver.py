"""
Save data prepared by microservice 2 in DynamoDB
@M-Malek
"""
# import boto3
import json
from shared.tools.log_logging import main_logger
from shared.tools.env_os_variables import aws_zip_bucket_name, aws_zip_object_key


def save_zip_data(client, data):
    """
    Save data extracted from .zip file in Amazon Web Services
    :param client: AWS Boto3 Client
    :param data: data to save in bucket
    :return: saving data in bucket or error
    """
    try:
        client.put_object(
            Bucket=aws_zip_bucket_name,
            Key=aws_zip_object_key,
            Body=json.dumps(data, ensure_ascii=False),
            ContentType="application/json"
        )
        main_logger("info", "ZIP data saved in AWS Bucket~!")
    except Exception as e:
        main_logger("error", f"Error during saving .zip data to AWS Bucket: {e}")
