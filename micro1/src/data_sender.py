"""

@M-Malek
"""

# Libs
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


# Small companion function to db management and connection check
def connection_checker(uri):
    """
    Check connection with database
    :param uri: connection string
    :return: Information if connection was successfully or Exception e if connection failed
    """
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        print("Connection successfully achieved!")
        client.close()
        return True
    except Exception as e:
        print("An error during a connection: " + e)
        return False


def db_data_wipeout(uri, tables):
    if not connection_checker(uri):
        print("Database currently unavailable. Data wipeout failed")
        return None

    print(f"Starting data wipeout from collections: {tables}")
    client = MongoClient(uri, server_api=ServerApi('1'))
    db_set = client["Poznan"]
    for table in tables:
        # Debug:
        # print(f"{table} type: {type(table)}")
        collection = db_set[table]
        collection.drop()
    client.close()
    print(f"Data wipe outed!")


def data_check(uri, tables):
    """
    Function to download small peace of data to check its quality
    :param uri: MongoDB connection uri
    :param tables: table name or tables names for which check data
    :return: list with data: each list element contains list of 5 data probe from tables described by tables
    """
    if not connection_checker(uri):
        print("Database currently unavailable. Data wipeout failed")
        return None

    result_list = []
    client = MongoClient(uri, server_api=ServerApi('1'))
    db_set = client["Poznan"]
    for table in tables:
        collection = db_set[table]
        random_docs = list(collection.aggregate([
            {"$sample": {"size": 5}}
        ]))
        result_list.append(random_docs)
    return result_list


# Main saving functions:
def save_vehicles(uri, data):
    """
    Save vehicles information to database
    :param uri: MongoDB Client URI
    :param data: pandas.DataFrame: prepared Vehicle data
    :return: nothing, saving data in db
    """
    if not connection_checker(uri):
        print("Database currently unavailable. Vehicles save failed")
        return None
    client = MongoClient(uri, server_api=ServerApi('1'))
    db_set = client["Poznan"]
    collection = db_set["Vehicles"]
    collection.insert_many(data.to_dict("records"))
    client.close()
