"""
Test error_handler
Test based on real-life DB from project testing
"""
from ztm_tools.sqs.consume.error_handler import error_handler
from ztm_tools.sqs.consume.connector import sqs_connector
from ztm_tools.sqs.consume.reader import sqs_message_reader
from os import environ
from json import loads


# Load S3_ENDPOINT to .env variables from hand
environ["S3_ENDPOINT"] = "" # delete after test / add to test!
environ["MONGO_URI"] = ""


def test_one():
    sqs = sqs_connector()
    message = sqs_message_reader(sqs, 'events', 'm3')
    message_own_id = loads(message['Body'])['task_id']
    #message_sqs_id = message['MessageId']
    error_handler(sqs, message)

    # Check if test is successful - check sqs queue status and check Mongo
    # Check SQS
    # status_queue_url = sqs.get_queue_url(QueueName="status")["QueueUrl"]
    message_after_work = sqs_message_reader(sqs, 'status', 'm3')
    message_own_after_work_id = loads(message_after_work['Body'])['task_id']
    assert message_own_id == message_own_after_work_id, 'Message not moved'

#Test passed
