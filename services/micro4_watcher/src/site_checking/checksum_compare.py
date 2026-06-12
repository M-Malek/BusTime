
def checksum_compare(checksum_new, checksum_old):
    """
    Compare checksum_new and checksum_old
    :param checksum_new: new checksum created from new zip file
    :param checksum_old: old checksum from MongoDB
    :return: True, when new checksum is not equal to old checksum, False otherwise, False if checksum_old is None
    """
    if checksum_old is None:
        return True
    if checksum_new != checksum_old:
        return True
    else:
        return False
