"""Tests for sqs_reader.py"""
from ztm_tools.sqs.consume.reader import sqs_message_reader
from ztm_tools.sqs.consume.connector import sqs_connector

"""
Function sqs_message_reader works if their result is a Message with type dict
"""
def test_sqs_message_reader():
    sqs = sqs_connector()
    message1 = sqs_message_reader(sqs, 'events', 'm3')
    assert type(message1) == dict, "Message not a dictionary - error"
    print(message1)

    message2 = sqs_message_reader(sqs, 'events', 'm2')
    assert type(message2) == dict, "Message not a dictionary - error"
    print(message2)
