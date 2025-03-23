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
    deep_sky_objects.extend(
        [
            DeepSkyObject(
                "Achernar", "Achernar", "Eridanus", "eruptive variable star", 0.42
            ),
            DeepSkyObject("Acrux", "Acrux", "Crux", "double star", 0.76),
            DeepSkyObject(
                "Aldebaran", "Aldebaran", "Taurus", "double star, variable star", 0.86
            ),
            DeepSkyObject(
                "Alnilam",
                "Alnilam",
                "Orion",
                "double star, pulsating variable star",
                1.65,
            ),
            DeepSkyObject("Alnitak", "Alnitak", "Orion", "double star", 1.85),
            DeepSkyObject(
                "Altair",
                "Altair",
                "Aquila",
                "double star, pulsating variable star",
                0.76,
            ),
            DeepSkyObject(
                "Antares",
                "Antares",
                "Scorpius",
                "double star, pulsating variable star",
                0.6,
            ),
            DeepSkyObject("Arcturus", "Arcturus", "Bootes", "double star", -0.05),
            DeepSkyObject("Bellatrix", "Bellatrix", "Orion", "double star", 1.60),
            DeepSkyObject(
                "Betelgeuse",
                "Betelgeuse",
                "Orion",
                "double star, pulsating variable star",
                0.50,
            ),
            DeepSkyObject("Capella", "Capella", "Auriga", "double star", 0.08),
            DeepSkyObject("Canopus", "Canopus", "Carina", "double star", -0.74),
            DeepSkyObject("Castor", "Castor", "Gemini", "double star", 1.90),
            DeepSkyObject(
                "Deneb", "Deneb", "Cygnus", "double star, pulsating variable star", 1.25
            ),
            DeepSkyObject(
                "Fomalhaut", "Fomalhaut", "Piscis Austrinus", "double star", 1.16
            ),
            DeepSkyObject(
                "Hadar",
                "Hadar",
                "Centaurus",
                "double star, pulsating variable star",
                0.61,
            ),
            DeepSkyObject(
                "Mintaka",
                "Mintaka",
                "Orion",
                "double star, eclipsing binary system",
                2.40,
            ),
            DeepSkyObject(
                "Polaris",
                "Polaris (North Star)",
                "Ursa Minor",
                "double star, pulsating variable star",
                1.98,
            ),
            DeepSkyObject("Pollux", "Pollux", "Gemini", "double star", 1.14),
            DeepSkyObject("Procyon", "Procyon", "Canis Minor", "double star", 0.34),
            DeepSkyObject("Regulus", "Regulus", "Leo", "double star", 1.35),
            DeepSkyObject(
                "Rigel", "Rigel", "Orion", "double star, pulsating variable star", 0.13
            ),
            DeepSkyObject("Sirius", "Sirius", "Canis Major", "double star", -1.46),
            DeepSkyObject(
                "Spica", "Spica", "Virgo", "double star, variable star", 0.97
            ),
            DeepSkyObject(
                "Vega", "Vega", "Lyra", "double star, pulsating variable star", 0.026
            ),
        ]
    )

    # other objects
    deep_sky_objects.extend(
        [
            DeepSkyObject("M33", "Triangulum Galaxy", "Triangulum", "galaxy", 5.70),
            DeepSkyObject("M31", "Andromeda Galaxy", "Andromeda", "galaxy", 3.40),
            DeepSkyObject("M42", "Great Orion Nebula", "Orion", "nebula", 4.00),
            DeepSkyObject(
                "M45",
                "Pleiades - Seven Sisters",
                "Taurus",
                "cluster (with nebulosity)",
                1.20,
            ),
            DeepSkyObject(
                "M3", "NGC 5272", "Canes Venatici", "globular star cluster", 3.40
            ),
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
                dso_object.constellation,
                dso_object.type,
                scinfo_altaz.alt,
                scinfo_altaz.az,
                dso_object.magnitude,
            )
        )
