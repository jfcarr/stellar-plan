# Stellar Plan

Stellar Plan uses [Astropy](https://www.astropy.org/) to generate an observing plan with information about bright stars, deep sky objects, and solar system objects.

## Setup

Install [uv](https://docs.astral.sh/uv/), if you haven't already.  Then, clone the project, initialize a virtual environment, and sync the packages:

```bash
git clone https://github.com/jfcarr/stellar-plan.git

cd stellar-plan

uv venv

uv sync
```

## Usage

In order to generate an observing plan, you must provide information about when (date/time and timezone) and where (latitude, longitude, and (optionally) height/elevation).  You can also provide an optional `--visible` argument to specify that you only want to include objects that are above the horizon.

For example, to generate a plan displaying visible items for Magdalena, New Mexico on July 22, 2025 at 10pm:

```bash
uv run stellar-plan-cli.py --latitude 34.123611 --longitude -107.236111 --datetime '2025-7-22 22:00:00' --timezone 'US/Mountain' --visible
```

Result:

Description | Constellation | Type | Altitude | Azimuth | Magnitude
------------|---------------|------|----------|---------|----------
Arcturus | Bootes | double star | 51.74 deg | 257.17 deg (West) | -0.05
Altair | Aquila | double star, pulsating variable star | 42.41 deg | 111.40 deg (East) | 0.76
Antares | Scorpius | double star, pulsating variable star | 29.11 deg | 186.32 deg (South) | 0.6
Polaris (North Star) | Ursa Minor | double star, pulsating variable star | 33.56 deg | 0.36 deg (North) | 1.98
Vega | Lyra | double star, pulsating variable star | 69.01 deg | 69.69 deg (East) | 0.026
Spica | Virgo | double star, variable star | 22.76 deg | 237.26 deg (South-West) | 0.97
Andromeda Galaxy | Andromeda | galaxy | 5.05 deg | 42.08 deg (North-East) | 3.4
NGC 5272 | Canes Venatici | globular star cluster | 48.83 deg | 275.37 deg (West) | 3.4
Mars | | planet | 9.02 deg | 269.05 deg (West) |

Refer to the Makefile for more examples.