from numpy import radians, cos

def lat_lng_to_meters(lat, lng, lat_ref=52.4):
    """
    Convert geographic coordinates to meters.
    :param lat: latitude
    :param lng: longitude
    :param lat_ref: reference latitude to calculations: default is 52.4 for Poznan, Wielkopolskie, Poland
    :return: x, y - coordinates in meters.
    """
    earth_radius = 6_371_000

    x = radians(lng) * earth_radius * cos(
        radians(lat_ref)
    )

    y = radians(lat) * earth_radius

    return x, y