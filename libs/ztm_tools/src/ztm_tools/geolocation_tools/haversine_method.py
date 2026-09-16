from math import asin, cos, radians, sin, sqrt

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    Note: default code from Google AI answer: https://www.google.com/search?q=haversine
    Source of Google AI answer: https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    :param lat1: latitude of first point
    :param lon1: longitude of first point
    :param lat2: latitude of second point
    :param lon2: longitude of second point
    :return: float, distance between two points in kilometers
    """
    r = 6_371_000

    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)

    delta_lat = radians(lat2 - lat1)
    delta_lng = radians(lon2 - lon1)

    a = (
            sin(delta_lat / 2) ** 2
            + cos(lat1_rad) * cos(lat2_rad)
            * sin(delta_lng / 2) ** 2
    )

    return 2 * r * asin(sqrt(a))
