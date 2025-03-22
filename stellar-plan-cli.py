import argparse
import astropy.units as u
from astropy.coordinates import (
    AltAz,
    Angle,
    EarthLocation,
    SkyCoord,
    get_body,
    get_moon,
)
from astropy.time import Time
from rich.console import Console
from rich.table import Table


class DeepSkyObject:
    def __init__(self, name, description, type, magnitude):
        self.name = name
        self.description = description
        self.type = type
        self.magnitude = magnitude


class SolarSystemObject:
    def __init__(self, name, description, type):
        self.name = name
        self.description = description
        self.type = type


class ResultObject:
    def __init__(self, description, object_type, altitude, azimuth, magnitude):
        self.description = description
        self.object_type = object_type
        self.altitude = altitude
        self.azimuth = azimuth
        self.magnitude = magnitude


def init_args_parse():
    parser = argparse.ArgumentParser(description="Generate an observing plan.")
    parser.add_argument(
        "--latitude", type=float, required=True, help="Latitude of observer's location"
    )
    parser.add_argument(
        "--longitude",
        type=float,
        required=True,
        help="Longitude of observer's location",
    )
    parser.add_argument(
        "--datetime",
        type=str,
        required=True,
        help="Date/time of observation plan. Example: '2025-4-5 21:00:00'",
    )
    parser.add_argument(
        "--utcoffset",
        type=int,
        required=True,
        help="UTC offset for local time. Example: -4 for Eastern Daylight Savings Time",
    )
    parser.add_argument(
        "--height", type=int, help="Height of observing location, in meters"
    )
    parser.add_argument(
        "--visible", action="store_true", help="Only include visible objects in plan"
    )

    return parser.parse_args()


def load_objects():
    deep_sky_objects = [
        DeepSkyObject("M33", "Triangulum Galaxy", "galaxy", 5.70),
        DeepSkyObject("M31", "Andromeda Galaxy", "galaxy", 3.40),
        DeepSkyObject("M42", "Great Orion Nebula", "nebula", 4.00),
        DeepSkyObject(
            "M45", "Pleiades - Seven Sisters", "cluster (with nebulosity)", 1.20
        ),
        DeepSkyObject("M3", "NGC 5272", "globular star cluster", 3.40),
        DeepSkyObject("Aldebaran", "Aldebaran", "double star, variable star", 0.85),
        DeepSkyObject("Capella", "Capella", "double star", 0.05),
        DeepSkyObject("Arcturus", "Arcturus", "double star", 0.15),
        DeepSkyObject(
            "Polaris",
            "Polaris (North Star)",
            "double star, pulsating variable star",
            1.95,
        ),
        DeepSkyObject("Sirius", "Sirius", "double star", -1.45),
        DeepSkyObject(
            "Betelgeuse", "Betelgeuse", "double star, pulsating variable star", 0.45
        ),
    ]

    solar_system_objects = [
        SolarSystemObject("moon", "Luna (Earth's Moon)", "moon"),
        SolarSystemObject("mercury", "Mercury", "planet"),
        SolarSystemObject("venus", "Venus", "planet"),
        SolarSystemObject("mars", "Mars", "planet"),
        SolarSystemObject("jupiter", "Jupiter", "planet"),
        SolarSystemObject("saturn", "Saturn", "planet"),
    ]

    return (deep_sky_objects, solar_system_objects)


def get_dso_info(dso_object):
    """
    Get information about a deep sky object.
    """
    scinfo = SkyCoord.from_name(dso_object.name)
    scinfo_altaz = scinfo.transform_to(AltAz(obstime=time, location=lewisburg))

    if not args.visible or (args.visible and scinfo_altaz.alt > 0):
        results.append(
            ResultObject(
                dso_object.description,
                dso_object.type,
                scinfo_altaz.alt,
                scinfo_altaz.az,
                dso_object.magnitude,
            )
        )


def get_sso_info(sso_object):
    """
    Get information about a solar system object.
    """
    bodyinfo = (
        get_moon(time) if sso_object.name == "moon" else get_body(sso_object.name, time)
    )
    bodyinfo_altaz = bodyinfo.transform_to(AltAz(obstime=time, location=lewisburg))

    if not args.visible or (args.visible and bodyinfo_altaz.alt > 0):
        results.append(
            ResultObject(
                sso_object.description,
                sso_object.type,
                bodyinfo_altaz.alt,
                bodyinfo_altaz.az,
                -99,
            )
        )


def format_altitude(altitude):
    return_value = f"{altitude:.2f}"

    if altitude <= 0:
        return_value = f"[red]{return_value} (below the horizon)[/red]"

    return return_value


def azimuth_to_cardinal(azimuth):
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


def display_table():
    console = Console()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Description")
    table.add_column("Type")
    table.add_column("Altitude")
    table.add_column("Azimuth")
    table.add_column("Magnitude")

    for result in sorted(results, key=lambda r: (r.object_type, r.description)):
        table.add_row(
            result.description,
            result.object_type,
            format_altitude(result.altitude),
            f"{result.azimuth:.2f} ({azimuth_to_cardinal(result.azimuth)})",
            f"{result.magnitude}" if result.magnitude != -99 else "",
        )

    print(f"Observation time (local) = {time + utcoffset}")
    console.print(table)


if __name__ == "__main__":
    args = init_args_parse()

    observer_latitude = args.latitude
    observer_longitude = args.longitude
    observer_height_in_meters = args.height if args.height else 0
    utc_offset_value = args.utcoffset
    observer_time_string = args.datetime

    (deep_sky_objects, solar_system_objects) = load_objects()

    results = []

    lewisburg = EarthLocation(
        lat=observer_latitude * u.deg,
        lon=observer_longitude * u.deg,
        height=observer_height_in_meters * u.m,
    )
    utcoffset = utc_offset_value * u.hour
    time = Time(observer_time_string) - utcoffset

    for dso in deep_sky_objects:
        get_dso_info(dso)

    for sso in solar_system_objects:
        get_sso_info(sso)

    display_table()
