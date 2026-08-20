from ztm_tools.sqs.consume.operation_decoder import operation_decoder

def test_operation_decoder():
    def function_with_param(text):
        print("Test for operation with param: text from param: ", text)

    def function_without_param():
        print("Test for operation without param")

    function_map = {
        'func1': function_with_param,
        'func2': function_without_param,
    }

    operation_payload1 = {'task': 'func1', 'text': "Its entry for test 111 222 \n 333"}
    operation_payload2 = {'task': 'func2'}

    operation1 = operation_decoder('func1', function_map, operation_payload1)
    operation2 = operation_decoder('func2', function_map, operation_payload2)
    assert operation1 == True, 'Function with param doesnt work'
    assert operation2 == True, 'Function without param doesnt work'

# Test passed
