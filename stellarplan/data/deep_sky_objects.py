from astropy.coordinates import AltAz, SkyCoord

from stellarplan.data.results import ResultObject


class DeepSkyObject:
    """
    Information about a deep sky object.
    """

    def __init__(self, name, description, type, magnitude):
        self.name = name
        self.description = description
        self.type = type
        self.magnitude = magnitude


def load_dso():
    """
    Load a list of deep sky objects.
    """
    deep_sky_objects = []

    # bright stars
    deep_sky_objects.extend(
        [
            DeepSkyObject("Aldebaran", "Aldebaran", "double star, variable star", 0.85),
            DeepSkyObject("Arcturus", "Arcturus", "double star", 0.15),
            DeepSkyObject(
                "Betelgeuse", "Betelgeuse", "double star, pulsating variable star", 0.45
            ),
            DeepSkyObject("Capella", "Capella", "double star", 0.05),
            DeepSkyObject(
                "Polaris",
                "Polaris (North Star)",
                "double star, pulsating variable star",
                1.95,
            ),
            DeepSkyObject("Sirius", "Sirius", "double star", -1.45),
        ]
    )

    # other objects
    deep_sky_objects.extend(
        [
            DeepSkyObject("M33", "Triangulum Galaxy", "galaxy", 5.70),
            DeepSkyObject("M31", "Andromeda Galaxy", "galaxy", 3.40),
            DeepSkyObject("M42", "Great Orion Nebula", "nebula", 4.00),
            DeepSkyObject(
                "M45", "Pleiades - Seven Sisters", "cluster (with nebulosity)", 1.20
            ),
            DeepSkyObject("M3", "NGC 5272", "globular star cluster", 3.40),
        ]
    )

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
                dso_object.type,
                scinfo_altaz.alt,
                scinfo_altaz.az,
                dso_object.magnitude,
            )
        )
