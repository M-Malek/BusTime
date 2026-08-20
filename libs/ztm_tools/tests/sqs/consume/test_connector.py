"""
Tests for ztm/sqs/consume/connector.py
"""
from ztm_tools.sqs.consume.connector import sqs_connector

from os import environ

# Load S3_ENDPOINT to .env variables from hand
environ["S3_ENDPOINT"] = "" # delete after test / add to test!

def test_one():
    """
    Tests for ztm/sqs/consume/connector.py - sqs message for worker in queue
    Note: test on a live sqs queue
    :return: assertion error if failed
    """
    sqs_conn = sqs_connector()
    assert sqs_conn is not None, 'sqs_conn is None'