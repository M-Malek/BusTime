"""
Tests for ztm/sqs/consume/connector.py
"""
from ztm_tools.sqs.consume.connector import sqs_connector

def test_one():
    """
    Tests for ztm/sqs/consume/connector.py - sqs message for worker in queue
    Note: test on a live sqs queue
    :return: assertion error if failed
    """
    sqs_conn = sqs_connector()
    assert sqs_conn is not None, 'sqs_conn is None'