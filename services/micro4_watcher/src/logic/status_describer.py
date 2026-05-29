from src.site_checking.ztm_site_checker import checksum_checker
from src.s3_checking.checker import s3_checker
from src.s3_checking.s3_connect import s3_connect


def get_status():
    checksum_bool = checksum_checker()
    s3 = s3_connect()
    s3_bool = s3_checker(s3)
    return status_describer(checksum_bool, s3_bool)


def status_describer(checksum_bool, s3_bool):
    """
    Describe logic for job_normal:
    - if there is new file on ZTM server and S3 is empty - download new data - return logic 1
    - if there is empty S3 - download new data - return logic 2
    - if there is new file on ZTM server and S3 isn't empty - empty S3 and download new data - return logic 3
    - if there isn't new file on ZTM server and S3 has data - skip - return logic 4
    """
    # print(f"Debug in logic: checksum_bool: {checksum_bool}, s3_bool: {s3_bool}"  )
    if checksum_bool and s3_bool:
        return 1

    if not checksum_bool and s3_bool or not s3_bool:
        return 2

    if not s3_bool and checksum_bool:
        return 3

    if not s3_bool and not checksum_bool:
        return 4
    # if s3_bool:
    #     return 2
    # if checksum_bool:
    #     if s3_bool:
    #         return 1
    #     if not s3_bool:
    #         return 3
    # if s3_bool == False and checksum_bool == False:
    #     return 4
    # return 5
    
    """if checksum_bool and s3_bool:
        return 1
    elif s3_bool:
        return 2
    elif checksum_bool and not s3_bool:
        return 3
    elif checksum_bool:
        return 4
    else:
        return None"""
