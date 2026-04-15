from src.site_checking.ztm_site_checker import checksum_checker
from src.s3_checking.checker import s3_checker


def status_describer(s3_object):
    """
    Describe status for job_normal:
    - if there is new file on ZTM server and S3 is empty - download new data - return status 1
    - if there is empty S3 - download new data - return status 2
    - if there is new file on ZTM server and S3 isn't empty - empty S3 and download new data - return status 3
    - if there isn't new file on ZTM server - skip - return status 4
    """
    if checksum_checker() and s3_checker(s3_object):
        return 1
    elif s3_checker(s3_object):
        return 2
    elif checksum_checker() and not s3_checker(s3_object):
        return 3
    elif checksum_checker():
        return 4
