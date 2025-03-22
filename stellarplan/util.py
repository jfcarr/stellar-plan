from astropy.coordinates import Angle


def format_altitude(altitude):
    """
    Create an altitude description string that indicates whether it is above or below the observer's horizon.
    """
    return_value = f"{altitude:.2f}"

    if altitude <= 0:
        return_value = f"[red]{return_value} (below the horizon)[/red]"

    return return_value


def azimuth_to_cardinal(azimuth):
    """
    Given an azimuth value (in degrees), return a text description of cardinal direction (e.g., North, South-West)
    """
    azimuth = Angle(azimuth).deg

    if azimuth >= 337.5 or azimuth < 22.5:
        return "North"
    elif 22.5 <= azimuth < 67.5:
        return "North-East"
    elif 67.5 <= azimuth < 112.5:
        return "East"
    elif 112.5 <= azimuth < 157.5:
        return "South-East"
    elif 157.5 <= azimuth < 202.5:
        return "South"
    elif 202.5 <= azimuth < 247.5:
        return "South-West"
    elif 247.5 <= azimuth < 292.5:
        return "West"
    elif 292.5 <= azimuth < 337.5:
        return "North-West"
