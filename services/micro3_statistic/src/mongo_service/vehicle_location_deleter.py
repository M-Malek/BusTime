from ztm_tools.logging.logger import main_logger
from ztm_tools.mongo_tools.mongo_connect import create_mongo_connection
from os import getenv

def db_data_wipeout(client, tables):
    """if not connection_checker(uri):
        # print("Database currently unavailable. Data wipeout failed")
        main_logger("error", "Database currently unavailable. Data wipeout failed")
        return None"""

    # print(f"Starting data wipeout from collections: {tables}")
    main_logger("warning", f"Starting data wipeout from collections: {tables}")
    con = create_mongo_connection(getenv("MONGO_URI"))
    db_set = client["Poznan"]
    for table in tables:
        # Debug:
        # print(f"{table} type: {type(table)}")
        collection = db_set[table]
        collection.drop()
    # client.close()
    # print(f"Data wipe outed!")
    main_logger("warning", "Data wipe outed!")