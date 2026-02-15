"""Observation data classes and parsers for various astrometric formats."""

import math
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Observation:
    """Single astrometric observation.

    Attributes:
        mjd: Modified Julian Date of the observation.
        ra: Right Ascension in degrees.
        dec: Declination in degrees.
        mag: Observed magnitude (0 = no magnitude).
        band: Photometric band character (default 'V').
        obscode: MPC 3-character observatory code.
        rms_ra: RA uncertainty in arcseconds (0 = use default).
        rms_dec: Dec uncertainty in arcseconds (0 = use default).
        spacebased: Whether this is a space-based observation.
        earth_obs: Earth-observer vector for space-based obs [x, y, z].
    """

    mjd: float
    ra: float
    dec: float
    mag: float = 0.0
    band: str = "V"
    obscode: str = "500"
    rms_ra: float = 0.0
    rms_dec: float = 0.0
    spacebased: bool = False
    earth_obs: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])

    @property
    def ra_rad(self) -> float:
        """RA in radians."""
        return math.radians(self.ra)

    @property
    def dec_rad(self) -> float:
        """Dec in radians."""
        return math.radians(self.dec)

    def to_tuple(self, site_index: int) -> tuple:
        """Convert to the tuple format expected by the C extension.

        Args:
            site_index: Integer site index from parse_obscode().

        Returns:
            Tuple of (mjd, ra_rad, dec_rad, vmag, site_int, rmsRA, rmsDec, spacebased).
        """
        return (
            self.mjd,
            self.ra_rad,
            self.dec_rad,
            self.mag,
            site_index,
            self.rms_ra,
            self.rms_dec,
            1 if self.spacebased else 0,
        )


# Magnitude band correction to V-band (same as common.c updateMagnitude)
_BAND_CORRECTIONS = {
    "V": 0.0,
    "B": -0.8,
    "U": -1.3,
    "g": -0.28,
    "r": 0.23,
    "R": 0.4,
    "C": 0.4,
    "W": 0.4,
    "i": 0.39,
    "z": 0.37,
    "I": 0.8,
    "J": 1.2,
    "w": -0.16,
    "y": 0.36,
    "L": 0.2,
    "H": 1.4,
    "K": 1.7,
    "Y": 0.7,
    "G": 0.24,
    "v": 0.0,
    "c": -0.05,
    "o": 0.33,
    "u": 2.5,
}


def _update_magnitude(band: str, mag: float) -> float:
    """Apply band correction to normalize magnitude to V-band."""
    if mag > 0:
        correction = _BAND_CORRECTIONS.get(band, -0.8)
        mag += correction
    return mag


def _date_to_mjd(year: int, month: int, day: float) -> float:
    """Convert calendar date to Modified Julian Date.

    Uses C-style integer division (truncation toward zero) to match
    the MPC80 parsing in d2mpc.c.
    """
    flookup = [0, 306, 337, 0, 31, 61, 92, 122, 153, 184, 214, 245, 275]
    z = year + int((month - 14) / 12)  # C-style truncation toward zero
    m = flookup[month] + 365 * z + z // 4 - z // 100 + z // 400 - 678882
    return m + day


def parse_mpc80(line: str) -> Optional[Observation]:
    """Parse an MPC 80-column format observation line.

    Args:
        line: An 80-column MPC format observation line.

    Returns:
        Observation object, or None if the line cannot be parsed.
    """
    if len(line) < 80:
        return None

    # Check note2 field for observation type
    note2 = line[14]
    if note2 not in ("C", "S", "B"):
        return None

    try:
        # Parse fields (right to left as in the C code)
        obscode = line[77:80]

        band = line[70]
        mag_str = line[65:70].strip()
        mag = float(mag_str) if mag_str else 0.0

        # Declination
        decs = float(line[51:56].strip())
        decm = int(line[48:50].strip())
        decd = int(line[45:47].strip())
        decg = line[44]

        # Right ascension
        ras = float(line[38:44].strip())
        ram = int(line[35:37].strip())
        rah = int(line[32:34].strip())

        # Date
        day = float(line[23:32].strip())
        month = int(line[20:22].strip())
        year = int(line[15:19].strip())

        # Designation
        desig = line[0:12]

    except (ValueError, IndexError):
        return None

    mjd = _date_to_mjd(year, month, day)
    ra_deg = (rah * 3600 + ram * 60 + ras) * 15.0 / 3600.0  # hours to degrees
    dec_deg = decd + decm / 60.0 + decs / 3600.0
    if decg == "-":
        dec_deg = -dec_deg

    vmag = _update_magnitude(band, mag)

    return Observation(
        mjd=mjd,
        ra=ra_deg,
        dec=dec_deg,
        mag=vmag,
        band=band,
        obscode=obscode,
    )


def parse_mpc80_file(filepath: str) -> Dict[str, List[Observation]]:
    """Parse an MPC 80-column format observation file.

    Groups observations by designation (first 12 characters of each line).

    Args:
        filepath: Path to the observation file.

    Returns:
        Dict mapping designation string -> list of Observations.
    """
    tracklets: Dict[str, List[Observation]] = {}

    with open(filepath, "r") as f:
        for raw_line in f:
            line = raw_line.rstrip("\n")
            if len(line) < 80:
                continue

            obs = parse_mpc80(line)
            if obs is None:
                continue

            desig = line[0:12]
            if desig not in tracklets:
                tracklets[desig] = []
            tracklets[desig].append(obs)

    return tracklets


def parse_ades_xml(filepath: str) -> Dict[str, List[Observation]]:
    """Parse an ADES XML observation file using Python's xml.etree.

    No libxml2 dependency required.

    Args:
        filepath: Path to the ADES XML file.

    Returns:
        Dict mapping designation/tracklet ID -> list of Observations.
    """
    import xml.etree.ElementTree as ET

    tree = ET.parse(filepath)
    root = tree.getroot()

    # Handle namespaces - ADES XML may use a default namespace
    ns = ""
    if root.tag.startswith("{"):
        ns = root.tag.split("}")[0] + "}"

    tracklets: Dict[str, List[Observation]] = {}

    def _process_optical(optical):
        """Process a single <optical> element and add to tracklets."""
        obs = _parse_ades_optical(optical, ns)
        if obs is not None:
            # Get tracklet sub-designation or provisional ID
            trkSub_el = optical.find(f"{ns}trkSub")
            provID_el = optical.find(f"{ns}provID")
            permID_el = optical.find(f"{ns}permID")

            desig = "unknown"
            if trkSub_el is not None and trkSub_el.text:
                desig = trkSub_el.text.strip()
            elif provID_el is not None and provID_el.text:
                desig = provID_el.text.strip()
            elif permID_el is not None and permID_el.text:
                desig = permID_el.text.strip()

            if desig not in tracklets:
                tracklets[desig] = []
            tracklets[desig].append(obs)

    # Find optical observations in obsBlock/obsData structure
    for obs_block in root.iter(f"{ns}obsBlock"):
        for obs_data in obs_block.iter(f"{ns}obsData"):
            for optical in obs_data.iter(f"{ns}optical"):
                _process_optical(optical)

    # Also find optical observations directly under root (flat ADES format)
    if not tracklets:
        for optical in root.iter(f"{ns}optical"):
            _process_optical(optical)

    return tracklets


def _parse_ades_optical(optical, ns: str) -> Optional[Observation]:
    """Parse a single ADES <optical> element."""
    try:
        # Required fields
        obsTime_el = optical.find(f"{ns}obsTime")
        ra_el = optical.find(f"{ns}ra")
        dec_el = optical.find(f"{ns}dec")
        stn_el = optical.find(f"{ns}stn")

        if obsTime_el is None or ra_el is None or dec_el is None or stn_el is None:
            return None

        # Parse ISO date to MJD
        obstime_str = obsTime_el.text.strip()
        mjd = _iso_to_mjd(obstime_str)

        ra_deg = float(ra_el.text.strip())
        dec_deg = float(dec_el.text.strip())
        obscode = stn_el.text.strip()

        # Optional fields
        mag = 0.0
        band = "V"
        mag_el = optical.find(f"{ns}mag")
        band_el = optical.find(f"{ns}band")
        if mag_el is not None and mag_el.text:
            mag = float(mag_el.text.strip())
        if band_el is not None and band_el.text:
            band = band_el.text.strip()

        vmag = _update_magnitude(band, mag)

        # RMS values
        rms_ra = 0.0
        rms_dec = 0.0
        rmsRA_el = optical.find(f"{ns}rmsRA")
        rmsDec_el = optical.find(f"{ns}rmsDec")
        if rmsRA_el is not None and rmsRA_el.text:
            rms_ra = float(rmsRA_el.text.strip())
        if rmsDec_el is not None and rmsDec_el.text:
            rms_dec = float(rmsDec_el.text.strip())

        return Observation(
            mjd=mjd,
            ra=ra_deg,
            dec=dec_deg,
            mag=vmag,
            band=band,
            obscode=obscode,
            rms_ra=rms_ra,
            rms_dec=rms_dec,
        )

    except (ValueError, AttributeError):
        return None


def _iso_to_mjd(iso_str: str) -> float:
    """Convert ISO 8601 datetime string to MJD.

    Handles formats like: 2022-12-25T09:14:20.544Z
    """
    # Remove trailing Z if present
    iso_str = iso_str.rstrip("Z")

    # Split date and time
    parts = iso_str.split("T")
    date_parts = parts[0].split("-")
    year = int(date_parts[0])
    month = int(date_parts[1])
    day_int = int(date_parts[2])

    fractional_day = 0.0
    if len(parts) > 1:
        time_parts = parts[1].split(":")
        hours = int(time_parts[0])
        minutes = int(time_parts[1]) if len(time_parts) > 1 else 0
        seconds = float(time_parts[2]) if len(time_parts) > 2 else 0.0
        fractional_day = (hours + minutes / 60.0 + seconds / 3600.0) / 24.0

    day = day_int + fractional_day
    return _date_to_mjd(year, month, day)
