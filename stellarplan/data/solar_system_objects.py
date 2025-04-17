import json
import os

from astropy.coordinates import AltAz, get_body

from stellarplan.data.results import ResultObject


class SolarSystemObject:
    """
    Information about a solar system object.
    """

    def __init__(self, name, description, type):
        self.name = name
        self.description = description
        self.type = type


def load_sso():
    """
    Load a list of solar system objects
    """
    solar_system_objects = []

    with open(
        os.path.join("stellarplan", "data", "store", "solar_system_objects.json"), "r"
    ) as file:
        data = json.load(file)
        solar_system_objects.extend([SolarSystemObject(**item) for item in data])

    return solar_system_objects


def get_sso_info(
    sso_object: SolarSystemObject,
    visible_only,
    observer_time,
    observer_location,
    results,
):
    """
    Get information about a solar system object.
    """
    bodyinfo = (
        get_body("moon", observer_time)
        if sso_object.name == "moon"
        else get_body(sso_object.name, observer_time)
    )
    bodyinfo_altaz = bodyinfo.transform_to(
        AltAz(obstime=observer_time, location=observer_location)
    )

    if not visible_only or (visible_only and bodyinfo_altaz.alt > 0):
        results.append(
            ResultObject(
                sso_object.description,
                "",
                sso_object.type,
                bodyinfo_altaz.alt,
                bodyinfo_altaz.az,
                -99,
            )
        )
