import hashlib

def calculate_checksum(response):
    """
    Calculate the checksum of the response content
    :param response_content: response.content from ZTM site
    :return:
    """
    hash_obj = hashlib.sha256()
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            hash_obj.update(chunk)

    checksum = hash_obj.hexdigest()
    return checksum