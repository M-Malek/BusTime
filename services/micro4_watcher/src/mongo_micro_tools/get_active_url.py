from ztm_tools.mongo_tools.mongo_connect import create_mongo_connection
from ztm_tools.logging.logger import main_logger
from datetime import datetime
from os import getenv


def get_active_url():
    """
    Get URL of .zip file which is active for today
    :return: str, URL to .zip file which is active for today (variable 'state' in MongoDB collection set to 'active')
    """
    def parse_date(doc):
        return datetime.strptime(doc["began_at"], "%Y%m%d")

    con = create_mongo_connection(getenv("MONGO_URI"))
    col = con["Poznan"]["Stop_times_arch"]

    docs = list(col.find({"state": "active"}))
    print(docs)
    if not docs:
        return None

    if len(docs) == 1:
        return docs[0].get("url")

    winner = min(docs, key=parse_date)

    main_logger(
        "error",
        "Detected more than one active URL! "
        "Selected earliest began_at."
    )

    return winner.get("url")
