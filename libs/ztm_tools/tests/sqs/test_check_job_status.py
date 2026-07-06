from ztm_tools.sqs.check_jobs_status import check_jobs_status

# GLOBALS
URI = "" # delete after tests!

def test_check_job_status():
    check_jobs_status(URI)