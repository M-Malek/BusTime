from site_checking.ztm_site_checker import ztm_site_checker
from site_checking.find_actual_schedule import find_actual_schedule
def ztm_watcher_logic():
    """
    Logic of ZTM site checking. Check ZTM site
    :return: state 1 and url when detected new file on ZTM site else 0, None
    """
    # 1. Check if there is new zip file
    new_schedule_bool = ztm_site_checker()
    # 2. Find actual url for site
    url = find_actual_schedule()
    if new_schedule_bool:
        return 1, url
    else:
        return 0, None
