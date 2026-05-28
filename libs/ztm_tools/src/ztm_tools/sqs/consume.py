from ztm_tools.sqs.receive_messages import receive_all_messages, delete_message
from os import getenv
from json import loads
from ztm_tools.logging.logger import main_logger


def consume(worker: str, FUNCTION_MAP: dict):
    """Consumes a messages from SQS queue for a given worker and executes the function specified in the message payload
       WARNING: This function requires the FUNCTION_NAP enviroment variable to be set!
    Args:
    worker (str): Worker name to fillter messsages by
    FUNCTION_MAP (dict): A dictionary mapping action names to functions to execute
    Returns:
        None
    """
    
    messages = receive_all_messages(worker)
    for message in messages:
        body = loads(message["Body"])

        action = body["action"]
        args = body.get("args", {})

        function = FUNCTION_MAP.get(action)

        if function is None:
            raise ValueError(
                f"Unknown action '{action}'"
            )
        function(**args)
        
        delete_message(message)


def test():
    print("To jest z twojej biblioteki!")
    