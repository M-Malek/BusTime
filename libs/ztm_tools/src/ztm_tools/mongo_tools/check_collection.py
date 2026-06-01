"""Check if collection has data"""

def check_collection(collection):
    count = collection.count()
    if count > 0:
        return "Collection with data"
    else:
        return "Collection with no data"