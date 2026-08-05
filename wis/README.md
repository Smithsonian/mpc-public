# wis

**Where Is Satellite/Observatory** – A Python package for calculating positions of observatories using NASA/JPL SPICE kernels.

## Why "wis"?

A traditional astronomical backronym:

* **W**here **I**s **S**atellite
* **W**here **I**s **S**atellite‑spice‑kernel
* **W**here **i**s **S**tation‑code/Observatory‑code
* (also) very light & **wis**py

## Overview

`wis` provides access to SPICE kernels' high‑precision observatory positions for both ground‑based and satellite observatories. It automatically downloads and manages the necessary SPICE kernels (NASA/JPL ephemeris data) and queries the MPC Observatory Codes API to obtain geocentric coordinates of ground stations.

### Key Features

* **Ground‑based observatory positions** – Supports all MPC observatory codes (e.g., `F51`, `W84`, `500` geocenter) via the MPC REST API.
* **Satellite observatory positions** – Currently supports TESS (`C57`), Kepler/K2 (`C55`), Gaia (`258`), Hubble Space Telescope (`250`), and James Webb Space Telescope (`274`) with extensible kernel specifications.
* **Multiple ephemeris files** – Choose between DE430 and DE440 ephemeris models via explicit kernel selection.
* **Automatic SPICE kernel management** – Kernels are downloaded to `~/.wispykernels/` and kept up‑to‑date (time‑critical files refreshed daily).
* **Explicit kernel loading** – Users specify exactly which kernels to load, improving startup performance.
* **Public methods**:
  * `get_obs_helio_equ_AU`
      - Returns heliocentric equatorial positions (AU) and light‑travel times (days) for a given MPC observatory code, falling back to obscode 500 (geocenter) if `fallback_to_geo` is set. Returns `None` if the code is not recognized and `fallback_to_geo=False`.
  * `get_bary_wrt_helio`
      - Returns Solar System barycenter position (AU), velocity (AU/day), and light‑travel time (days) relative to the heliocenter.
  * see below for examples

## Installation

### From source (recommended for development)

```bash
git clone https://github.com/Smithsonian/mpc-public.git
cd mpc-public/wis
pip install .
```

## Usage

### Basic Example (Ground Observatories)

```python
from wis import Wis
from wis.kernels import DE430
from astropy.time import Time

# Create a Wis context manager with DE430 kernel
with Wis(kernels=DE430) as w:
    # Get heliocentric equatorial positions for Pan‑STARRS 1 (F51)
    # at two Julian dates (TDB scale)
    obscode = "F51"
    times = Time([2451545.000742869, 2451546.000742869], format="jd", scale="tdb")

    pos, ltt = w.get_obs_helio_equ_AU(obscode, times)
    # pos: shape (N,3) array of positions [AU]
    # ltt: shape (N,) array of light‑travel times [days]

    print(f"Positions [AU]:\n{pos}")
    print(f"Light‑travel times [days]:\n{ltt}")

    # Position of barycenter wrt heliocenter
    bary_pos, bary_vel, bary_ltt = w.get_bary_wrt_helio(times)
    # bary_pos: shape (N,3) position vectors [AU]
    # bary_vel: shape (N,3) velocity vectors [AU/day]
    # bary_ltt: shape (N,) light‑travel times [days]
```

### Loading Multiple Kernels (Ground + Satellite)

```python
from wis import Wis
from wis.kernels import DE430, TESS
from astropy.time import Time

# Load both ground and satellite kernels
with Wis(kernels=[DE430, TESS]) as w:
    # Calculate TESS position
    times = Time([2458337.829157830], format="jd", scale="tdb")
    pos, ltt = w.get_obs_helio_equ_AU("C57", times)
    print(f"TESS position [AU]:\n{pos}")

    # Can also calculate ground observatory positions
    pos_f51, ltt_f51 = w.get_obs_helio_equ_AU("F51", times)
    print(f"Pan-STARRS position [AU]:\n{pos_f51}")
```

### Using DE440 Ephemeris

```python
from wis import Wis
from wis.kernels import DE440
from astropy.time import Time

times = Time([2451545.000742869, 2451546.000742869], format="jd", scale="tdb")
with Wis(kernels=DE440) as w:
    # Use DE440 instead of DE430
    pos, ltt = w.get_obs_helio_equ_AU("500", times)
```

### Creating Custom Kernels

You can create custom `KernelSpecifier` objects for other satellites or observatories:

```python
from wis import Wis
from wis.kernelspecifier import KernelSpecifier
from wis.kernels import DE430  # Still need ground kernel for Earth position
from astropy.time import Time

# Define a custom kernel for your satellite
MySatelliteKernel = KernelSpecifier(
    obscodeMPC="C99",
    obscodeJPL="-999",
    name="MySatellite",
    files=["https://example.com/mysatellite.bsp"],
    wildcards={},
    timecritical=[]
)

times = Time([2458337.829157830], format="jd", scale="tdb")
# Use it alongside built-in kernels
with Wis(kernels=[DE430, MySatelliteKernel]) as w:
    pos, ltt = w.get_obs_helio_equ_AU("C99", times)
```

## Supported Observatories

### Ground‑Based Observatories

All MPC observatory codes are supported. The geocentric coordinates are retrieved from the MPC REST API (`https://data.minorplanetcenter.net/api/obscodes`) and cached locally for one day. Codes that use two‑line observations are flagged and excluded from position calculations.

### Satellite Observatories

| MPC Code | Name  | NAIF ID | Kernel Source |
|----------|-------|---------|---------------|
| `C57`    | TESS  | `-95`   | STScI archive |
| `C55`    | Kepler | `-227`  | STScI archive |
| `258`    | Gaia  | `-123`  | ESA SPICE archive |
| `250`    | HST   | `-48`   | NAIF HST archive |
| `274`    | JWST  | `-170`  | NAIF JWST archive |

Additional satellites can be added by creating custom `KernelSpecifier` objects or by extending the satellite definitions in your own module (see CLI section below).

## Kernel Management

### Explicit Kernel Loading

Unlike previous versions, `wis` now requires you to explicitly specify which kernels to load. This improves startup performance and gives you full control over which SPICE data is downloaded and loaded into memory.

```python
from wis import Wis
from wis.kernels import DE430, DE440, KEPLER, TESS, GAIA, HST, JWST

# Load only what you need
with Wis(kernels=DE430) as w:           # Ground only
    pass
with Wis(kernels=[DE430, TESS]) as w:   # Ground + TESS
    pass
with Wis(kernels=[DE440, KEPLER, TESS]) as w:  # Ground (DE440) + KEPLER + TESS
    pass
```

> **Note:** A ground kernel (`DE430` or `DE440`) is always required. It supplies the leapsecond file for time conversion and the planetary ephemeris needed to compute heliocentric positions. `Wis(kernels=TESS)` alone will raise a `ValueError` at startup.

### Automatic Download & Loading

When a `Wis` instance is entered (the `__enter__` method), it:

1. Downloads any missing or out-of-date kernel files for the specified kernels.
2. Loads all necessary kernels into SPICE memory.

Kernels are stored in `~/.wispykernels/`. Each kernel has its own subdirectory. Time‑critical files (e.g., `earth_latest_high_prec.bpc`) are refreshed every 24 hours; other files are considered static.

### Command‑Line Download Utility

A script `download-wis-kernels` is installed with the package. It downloads specified kernels without loading them.

```bash
# List available built-in kernels
download-wis-kernels --list

# Download specific kernels
download-wis-kernels DE430
download-wis-kernels DE430 TESS
download-wis-kernels DE430 DE440 KEPLER TESS GAIA HST JWST

# Download with custom kernels from a Python module
download-wis-kernels --module mypackage.kernels DE430 MyCustomKernel
```

This is useful for pre‑populating the kernel cache in Docker images or CI environments.

### Kernel Metadata

Each `KernelSpecifier` maintains a JSON metadata file (`kernel_filepath_map.json`) that records the remote URL, download date, file size, and MD5 hash of each kernel. This metadata is used to decide whether a file needs to be re‑downloaded.

#### Ground‑Based Kernels (DE430 & DE440)

| Path / Wildcard | Ephemeris | Refresh | Purpose |
|-----------------|-----------|---------|---------|
| `https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/latest_leapseconds.tls` | Both | Static | Leap‑seconds |
| `https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/pck00011.tpc` | Both | Static | Planetary constants |
| `https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_latest_high_prec.bpc` | Both | **Daily** | High‑precision Earth orientation (time‑critical) |
| `https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_*_combined.bpc` (wildcard) | Both | Static | Combined Earth orientation predictions+reconstructions |
| `https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de430.bsp` | DE430 only | Static | DE430 planetary ephemeris |
| `https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/gm_de431.tpc` | DE430 only | Static | DE431 GM constants |
| `https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de440.bsp` | DE440 only | Static | DE440 planetary ephemeris |
| `https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/gm_de440.tpc` | DE440 only | Static | DE440 GM constants |

*Static* kernels are downloaded once and never automatically refreshed (unless manually deleted).
*Daily* kernels are re‑downloaded if older than 24h.

#### Satellite Kernels

| Satellite | MPC Code | Path / Wildcard | Refresh | Notes |
|-----------|----------|-----------------|---------|-------|
| TESS | C57 | `https://archive.stsci.edu/missions/tess/models/TESS_EPH_DEF*` (wildcard) | Static | Kernel list from 2019; may be outdated |
| Kepler | C55 | `https://archive.stsci.edu/pub/k2/spice/kplr2018134232543.tsc` | Static | Kepler spacecraft clock |
| Kepler | C55 | `https://archive.stsci.edu/pub/k2/spice/spk_2018290000000_2018306220633_kplr.bsp` | Static | Kepler ephemeris (2018‑2019) |
| Gaia | 258 | `https://spiftp.esac.esa.int/data/SPICE/GAIA/kernels/spk/gaia_flp_20131219_21250328_v01.bsp` | Static | Reconstructed mission trajectory, then long prediction |
| HST | 250 | `https://naif.jpl.nasa.gov/pub/naif/HST/kernels/spk/hst.bsp` | **Daily** | Current HST trajectory |
| JWST | 274 | `https://naif.jpl.nasa.gov/pub/naif/JWST/kernels/spk/jwst_pred.bsp` | **Daily** | Predicted trajectory; loaded before reconstructed data |
| JWST | 274 | `https://naif.jpl.nasa.gov/pub/naif/JWST/kernels/spk/jwst_rec.bsp` | **Daily** | Reconstructed trajectory; loaded after predicted data so it wins in overlap |

Static satellite kernels are downloaded once and never automatically refreshed (note that the TESS mission adds new kernels periodically, and these will be discovered/downloaded if not present locally). Daily satellite kernels are re‑downloaded if older than 24h.

## Migration Guide (Breaking Changes)

**Version 2.0.0 introduces breaking changes from earlier versions:**

### Old API (no longer supported)
```python
# OLD - Automatically loaded all kernels
with Wis() as w:
    pass

# OLD - Used ephemeris parameter
with Wis(ephemeris="DE440") as w:
    pass

# OLD - Environment variable controlled ephemeris
import os
os.environ['EPHEMERIS'] = 'DE440'
with Wis() as w:
    pass
```

### New API
```python
from wis import Wis
from wis.kernels import DE430, DE440, KEPLER, TESS, GAIA, HST, JWST

# NEW - Must explicitly specify kernels
with Wis(kernels=DE430) as w:
    pass

# NEW - Use DE440 ephemeris
with Wis(kernels=DE440) as w:
    pass

# NEW - Multiple kernels
with Wis(kernels=[DE430, TESS]) as w:
    pass
```

### CLI Changes
```bash
# OLD - Downloaded all kernels by default
download-wis-kernels

# NEW - Must specify which kernels to download
download-wis-kernels DE430 TESS

# NEW - List available kernels
download-wis-kernels --list
```

## Development

### Running Tests

```bash
pytest tests/
```

Tests include unit tests for individual modules and integration tests that verify kernel downloads and position calculations.


## Future work

* Add more satellite kernels
* Better caching (currently a local cache for entire call signatures; could be remote-friendly, as well as individual times)
* Add more unit tests
* Provide a Docker image with pre‑downloaded kernels
