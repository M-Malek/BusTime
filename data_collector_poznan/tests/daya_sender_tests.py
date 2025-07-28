from data_collector_poznan.src.db_sender.data_sender import connection


# Test 1: try connection to data_server
def sender_test_1():
    """
    Test connection to data server
    :return: Log "Connection successfully achieved!" if connection was successfully.
    """
    uri = "here pass connection string!"
    connection(uri)

sender_test_1()

"""
Tests result:
No. 1 - ok
No. 2 - 
"""
