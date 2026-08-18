"""
Decode and accomplish work
:author: @M-Malek
"""
from ztm_tools.logging.logger import main_logger

def operation_decoder(operation, function_map, operation_payload):
    """
    Find in function map and do an operation
    :param operation: str, operation to do
    :param function_map: dict, function_map dictionary
    :param operation_payload: dict, operation payload dictionary
    :return: True if task accomplished, False otherwise
    """
    # 1. Delete parameter 'task' from operation_payload - 'task' is an operation!
    operation_payload.pop('operation')

    function = function_map.get(operation)
    if function:
        try:
            function(**operation_payload)
        except Exception as e:
            main_logger("error", f"Error during accomplish operation {operation}: \n {e}")
            return False
    else:
        main_logger("error", f"There is no operation: {operation} in function_map")
        return False
            