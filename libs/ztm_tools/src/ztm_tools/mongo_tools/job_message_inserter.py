import pymongo

def job_message_inserter(collection, message):
    attempts = 0
    error_messages = []
    while attempts < 5:
        try:
            _id = collection.insert_one(message)
            return _id.inserted_id
        except Exception as e:
            error_messages.append(e)
        attempts += 1
    return error_messages