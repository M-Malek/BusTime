def check_pending_state(collection):
    """
    Return all collection with pending state data
    :param collection: collection to check
    :return: id of all documents with state equals to pending
    """
    results = collection.find({"state": "pending"})
    return results
