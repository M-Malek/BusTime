from datetime import datetime

def entry_creator(collection, new_checksum, filename: str, created_at, began_at, url: str, state: str):
    """
    Prepare and send entry for Poznań ZTM Stop_times_archive collection
    :param collection: MongoDB collection: stop_times_arch
    :param new_checksum: sha256 checksum of new ZTM file
    :param filename: filename of new ZTM file: .zip name
    :param created_at: date of entry
    :param url: url of ZTM .zip file
    :param state: state of entry
    :return: MongoDB collection updated
    """
    new_entry = collection.insert_one({
        "checksum": new_checksum,
        "file_name": filename,
        "created_at": created_at,
        "began_at": began_at,
        "url": url,
        "state": state
    })
    return new_entry.inserted_id