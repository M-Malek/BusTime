from ztm_tools.sqs.receive_messages import receive_all_messages

def check_messages(functions_map):
    messages = receive_all_messages("m3")
    for message in messages:
        print("-------------------------------------")
        print(message)
    #print(messages)
