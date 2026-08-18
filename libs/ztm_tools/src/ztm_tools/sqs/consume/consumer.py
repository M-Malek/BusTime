"""
Main function to collect and handle SQS Messages
:author: @M-Malek
"""
from ztm_tools.sqs.consume.connector import sqs_connector
from ztm_tools.sqs.consume.reader import sqs_message_reader
from ztm_tools.sqs.consume.operation_decoder import operation_decoder
from ztm_tools.sqs.consume.error_handler import error_handler
from ztm_tools.mongo_tools.set_work_done_in_mongo import set_work_done_in_mongo
from ztm_tools.logging.logger import main_logger

def message_consumer(worker, queue, function_map):
    """
    Function to handle SQS Messages
    :param worker: str, name of worker
    :param queue: str, name of queue
    :param function_map: dict, key-value pairs of name and function to be executed
    :return: Read and do actions from SQS Message base on function_map
    """

    # 1. Connect to SQS message queue
    print("Debug: message_consumer is running")
    sqs = sqs_connector()
    queue_url = sqs.get_queue_url(QueueName=queue)["QueueUrl"]
    print("Debug: SQS Queue URL: ", queue_url)
    while True:
        try:
            # 2. Read message to given worker
            message = sqs_message_reader(sqs, queue, worker)
            print("Debug: SQS Message Read: ", message)
            operation = message['payload']['task']
            operation_payload = message['payload']
            # message_body = message["Body"]
            # receipt_handle = message["ReceiptHandle"]
            # message_id = message["MessageId"]

            # 3. Try to accomplish work
            for attempt in range(1, 4):
                # Try to do an action
                operation_status = operation_decoder(operation, function_map, operation_payload)
                # 4. If work passed - change status, go next
                print("Debug: Operation status: ", operation_status)
                if operation_status:
                    main_logger("info", f"Operation: {operation}: success!")
                    set_work_done_in_mongo(message, "accomplished")
                    sqs.delete_message(
                        QueueUrl=queue_url,
                        ReceiptHandle=message["ReceiptHandle"]
                    )
                    break
                # 5. If work failed - error_handler
                if attempt == 3:
                    print("Debug: Error in operation: ", operation)
                    error_handler(message, operation, operation_payload)
        except StopIteration:
            break
