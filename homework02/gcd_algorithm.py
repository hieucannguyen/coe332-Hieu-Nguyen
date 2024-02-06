from math import acos, cos, sin, pi

def great_circle_distance(point1: tuple, point2: tuple) -> float:
    """
    Computes the distance between meteors given 2 latitude and longitude points using
    the great circle distance formula

    Args:
        point1 (tuple): latitude and longitude of the first meteorite
        point2 (tuple): latitude and longitude of the second meteorite

    Returns:
        distance (float): great circle distance of the two points
    """
    latitude1, longitude1 = point1
    latitude2, longitude2 = point2

    if latitude1 > 90 or latitude2 > 90 or latitude1 < -90 or latitude2 < -90:
        raise ValueError
    if longitude1 > 180 or longitude2 > 180 or longitude1 < -180 or longitude2 < -180:
        raise ValueError
    
    # Convert to radians
    latitude1 = latitude1 * pi / 180
    longitude1 = longitude1 * pi / 180
    latitude2 = latitude2 * pi / 180
    longitude2 = longitude2 * pi / 180

    delta_longitude = abs(longitude1-longitude2)

    # Compute central angle
    central_angle = acos(sin(latitude1)*sin(latitude2) + cos(latitude1)*cos(latitude2)*cos(delta_longitude))

    return 6378.137*central_angle
