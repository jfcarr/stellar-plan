import json
import os

from astropy.coordinates import AltAz, SkyCoord

from stellarplan.data.results import ResultObject


class DeepSkyObject:
    """
    Information about a deep sky object.
    """

    def __init__(self, name, description, constellation, type, magnitude):
        self.name = name
        self.description = description
        self.constellation = constellation
        self.type = type
        self.magnitude = magnitude


def load_dso():
    """
    Load a list of deep sky objects.
    """
    deep_sky_objects = []

    # bright stars
    with open(
        os.path.join("stellarplan", "data", "store", "deep_sky_objects_stars.json"), "r"
    ) as file:
        data = json.load(file)
        deep_sky_objects.extend([DeepSkyObject(**item) for item in data])

    # other objects
    with open(
        os.path.join("stellarplan", "data", "store", "deep_sky_objects_other.json"), "r"
    ) as file:
        data = json.load(file)
        deep_sky_objects.extend([DeepSkyObject(**item) for item in data])

    return deep_sky_objects


def get_dso_info(
    dso_object: DeepSkyObject, visible_only, observer_time, observer_location, results
):
    """
    Get information about a deep sky object.
    """
    scinfo = SkyCoord.from_name(dso_object.name)
    scinfo_altaz = scinfo.transform_to(
        AltAz(obstime=observer_time, location=observer_location)
    )

    if not visible_only or (visible_only and scinfo_altaz.alt > 0):
        results.append(
            ResultObject(
                dso_object.description,
                dso_object.constellation,
                dso_object.type,
                scinfo_altaz.alt,
                scinfo_altaz.az,
                dso_object.magnitude,
            )
        )
