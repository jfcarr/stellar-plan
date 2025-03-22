import argparse
from datetime import datetime

import astropy.units as u
import pytz
from astropy.coordinates import EarthLocation
from astropy.time import Time
from rich.console import Console
from rich.table import Table

from stellarplan.data.deep_sky_objects import get_dso_info, load_dso
from stellarplan.data.solar_system_objects import get_sso_info, load_sso
from stellarplan.util import azimuth_to_cardinal, format_altitude


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
        "--timezone",
        type=str,
        required=True,
        help="Timezone of observer. Example: 'America/New_York'",
    )
    parser.add_argument(
        "--height", type=int, help="Height of observing location, in meters"
    )
    parser.add_argument(
        "--visible", action="store_true", help="Only include visible objects in plan"
    )

    return parser.parse_args()


def display_table():
    console = Console()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Description")
    table.add_column("Constellation")
    table.add_column("Type")
    table.add_column("Altitude")
    table.add_column("Azimuth")
    table.add_column("Magnitude")

    for result in sorted(results, key=lambda r: (r.object_type, r.description)):
        table.add_row(
            result.description,
            result.constellation,
            result.object_type,
            format_altitude(result.altitude),
            f"{result.azimuth:.2f} ({azimuth_to_cardinal(result.azimuth)})",
            f"{result.magnitude}" if result.magnitude != -99 else "",
        )

    console.print(table)


if __name__ == "__main__":
    args = init_args_parse()

    observer_latitude = args.latitude
    observer_longitude = args.longitude
    observer_height_in_meters = args.height if args.height else 0
    observer_time_string = args.datetime
    observer_timezone_string = args.timezone

    deep_sky_objects = load_dso()
    solar_system_objects = load_sso()

    observer_location = EarthLocation(
        lat=observer_latitude * u.deg,
        lon=observer_longitude * u.deg,
        height=observer_height_in_meters * u.m,
    )

    naive_datetime = datetime.strptime(observer_time_string, "%Y-%m-%d %H:%M:%S")

    timezone = pytz.timezone(observer_timezone_string)
    localized_datetime = timezone.localize(naive_datetime)

    observer_time = Time(localized_datetime)

    results = []

    for dso in deep_sky_objects:
        get_dso_info(dso, args.visible, observer_time, observer_location, results)

    for sso in solar_system_objects:
        get_sso_info(sso, args.visible, observer_time, observer_location, results)

    print(f"Observation time (local) = {observer_time_string}")
    display_table()
