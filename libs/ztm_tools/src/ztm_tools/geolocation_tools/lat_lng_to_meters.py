import numpy as np

def lat_lng_to_meters(lat, lng, lat_ref=52.4):
    """
    Convert geographic coordinates to meters.
    :param lat: latitude
    :param lng: longitude
    :param lat_ref: reference latitude to calculations: default is 52.4 for Poznan, Wielkopolskie, Poland
    :return: x, y - coordinates in meters.
    """
    earth_radius = 6_371_000

    # Pandas/Mongo inputs can arrive as object arrays. np.radians does not
    # apply its numeric loop to arrays of Python objects, even when each item
    # is a float, so normalize the input dtype first.
    lat = np.asarray(lat, dtype=np.float64)
    lng = np.asarray(lng, dtype=np.float64)
    lat_ref = np.asarray(lat_ref, dtype=np.float64)

    x = np.radians(lng) * earth_radius * np.cos(np.radians(lat_ref))
    y = np.radians(lat) * earth_radius

    return x, y
