"""Tests for recive_messages.py and consume.py modules"""
from ztm_tools.sqs.receive_messages import receive_all_messages, delete_message
from ztm_tools.sqs.consume import consume
from unittest.mock import patch, MagicMock


# GLOBAL VARIABLES
SQS_MESSAGE = {'event_id': '7b40a1fa-55fb-464d-bdbd-fa84fb16d857', 'event_type': 'STATISTIC_NORMAL', 'source': 'micro4_watcher', 'timestamp': '2026-05-26T18:25:26.528271+00:00', 'payload': {'worker': 'microservice_3', 'changed_data': {'type': 'vehicles_stats', 'action': 'statistic', 'location': 'MONGODB/stats'}}}


@patch("ztm_tools.src.ztim_tools.sqs.recieve_message")
def test_receive_all_messages():
    pass


@patch('ztm_tools.src.ztm_tools.sqs.consume.sqs')
def test_delete_message(mock_sqs):
    delete_message(
        "queue_url",
        "receipt_handle"
    )

    mock_sqs.delete_message.assert_called_once_with(
        QueueUrl="queue_url",
        ReceiptHandle="receipt_handle"
    )

def test_consume():
    pass