from ztm_tools.mongo_tools.mongo_connect import create_mongo_connection
from ztm_tools.models.trip_progress import TripProgress
from os import getenv


def take_mongo_data(trip_id, route_id, data_object=None):
    """
    Connect to MongoDB and download/save TripProgress
    if data_object == None: function download data from MongoDB
    if data_object != None: function save data to MongoDB
    :param trip_id: id of trip
    :param route_id: id of route
    :param data_object: object to save, optional
    :return:
    """
    if data_object:
        # Function will save data
        con = create_mongo_connection(getenv("MONGO_URI"))
        col = con['Poznan']['Line_info']
        if col.find_one({"trip_id": trip_id}):
            col.update_one({"trip_id": trip_id}, {"$set": data_object}, upsert=False)
        else:
            col.insert_one(data_object)
        con.close()
        return data_object
    else:
        # data_object is None so function will download data:
        con = create_mongo_connection(getenv("MONGO_URI"))
        col = con['Poznan']['Line_info']
        if col.find_one({"trip_id": trip_id}):
            processing = col.find_one({"shape_id": trip_id})
            current_trip = TripProgress.from_dict(processing)
        else:
            current_trip = TripProgress(
                trip_id,
                route_id,
                None)
        con.close()
        return current_trip
