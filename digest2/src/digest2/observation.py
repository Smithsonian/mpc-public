"""Observation data classes and parsers for various astrometric formats."""

import math
from datetime import datetime
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
        earth_obs: Geocentric equatorial observer position [x, y, z] in AU,
            used instead of the observatory parallax constants when
            spacebased is True.
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
            Tuple of (mjd, ra_rad, dec_rad, vmag, site_int, rmsRA, rmsDec,
            spacebased, earth_obs_x, earth_obs_y, earth_obs_z).
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
            self.earth_obs[0],
            self.earth_obs[1],
            self.earth_obs[2],
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


# km -> AU scale factor, computed as in d2ades.c / d2mpc.c (sf = 1 / 1 AU in km)
# so that converted positions are bit-identical to the C parsers.
_KM_TO_AU = 1 / 149.59787e6


def _roving_position(x: float, y: float, altitude: float) -> List[float]:
    """Convert a roving-observer position to a geocentric vector.

    Exact reimplementation of roving_position() in d2math.c, kept
    bit-compatible so the Python wrapper scores identically to the C CLI.
    """
    a = 6378137.0
    b = 6356752.314245
    numerator = (a * a * math.cos(y)) ** 2 + (b * b * math.sin(y)) ** 2
    denominator = (a * math.cos(y)) ** 2 + (b * math.sin(y)) ** 2
    r = math.sqrt(numerator / denominator) + altitude
    return [
        r * math.cos(x) * math.cos(y),
        r * math.cos(x) * math.sin(y),
        r * math.sin(x),
    ]


def _observer_position(sys: Optional[str], pos1: Optional[str],
                       pos2: Optional[str], pos3: Optional[str]):
    """Derive (spacebased, earth_obs) from ADES sys/pos1/pos2/pos3 fields.

    Mirrors the satellite/roving handling in d2ades.c (processOptical):

    - All four fields must be present, otherwise the observation is
      treated as ground-based.
    - ``sys`` containing ``_KM`` (e.g. ICRF_KM): positions are km,
      converted to AU.
    - ``sys`` containing ``WGS84`` (roving observer): positions are
      converted via _roving_position() then scaled like km.
    - Any other ``sys`` (e.g. ICRF_AU): positions are used as-is (AU).

    Returns:
        (spacebased, earth_obs) tuple; (False, [0, 0, 0]) if the fields
        are absent or unparseable.
    """
    if not (sys and pos1 and pos2 and pos3):
        return False, [0.0, 0.0, 0.0]

    try:
        x = float(pos1)
        y = float(pos2)
        z = float(pos3)
    except ValueError:
        return False, [0.0, 0.0, 0.0]

    is_satellite = "_KM" in sys
    is_roving = "WGS84" in sys

    if is_roving:
        x, y, z = _roving_position(x, y, z)

    if is_satellite or is_roving:
        x *= _KM_TO_AU
        y *= _KM_TO_AU
        z *= _KM_TO_AU

    return True, [x, y, z]


def _date_to_mjd(year: int, month: int, day: float) -> float:
    """Convert calendar date to Modified Julian Date.

    This intentionally reimplements the exact algorithm from d2mpc.c
    (parseMpc80, lines 170-174) rather than using astropy.time.Time,
    for three reasons:

    1. **Bit-exact C parity.**  The Python package wraps the C scoring
       engine.  The MJD produced here is passed to the C extension and
       must match the value that the C CLI computes for the same input
       line, otherwise the two would give different scores for the same
       observation file.

    2. **No heavy dependency.**  astropy is ~200 MB installed; this
       package intentionally depends only on numpy.

    3. **Timescale sophistication is unnecessary.**  MPC 80-column
       dates carry at most ~6 fractional-day digits (~0.1 s precision).
       The C code treats the conversion as pure calendar arithmetic
       with no leap-second or UTC/TT distinction.

    Note on integer division: C truncates toward zero, Python floors
    toward negative infinity.  For months <= 13 the term
    ``(month - 14) / 12`` is negative, so we use ``int(... / 12)``
    (float division then truncation) instead of ``// 12``.  The
    remaining ``z // 4`` etc. terms are safe because *z* (a year
    number) is always positive.
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


def _c_strtod(s: str) -> float:
    """Parse a float like mustStrtod in d2mpc.c.

    An optional leading sign may be separated from the digits by
    whitespace (e.g. ``"- 3471.6659"``), as found in some MPC 80-column
    satellite position lines.
    """
    neg = s.startswith("-")
    if neg or s.startswith("+"):
        s = s[1:]
    value = float(s)
    return -value if neg else value


def _apply_mpc80_second_line(line: str, obs: Observation) -> bool:
    """Apply an 80-column second line to the preceding observation.

    Satellite observations (note2 'S') and roving observations (note2 'V')
    are followed by a second line (note2 's' / 'v') carrying the observer
    position in columns 35-69.  This mirrors parseMpcSat / parseMpcRoving
    in d2mpc.c: the position is attached to the preceding observation as a
    geocentric vector in AU and the observation is marked space-based.

    Returns:
        True if the position was applied, False if the line was rejected.
    """
    note2 = line[14]
    try:
        x = _c_strtod(line[34:45])
        y = _c_strtod(line[46:57])
        z = _c_strtod(line[58:69])
    except ValueError:
        return False

    if note2 == "s":
        # parseMpcSat: obscode must match the observation being amended;
        # column 33 flags the units ('1' = km, '2' = AU).
        if line[77:80] != obs.obscode:
            return False
        if line[32] == "1":
            x *= _KM_TO_AU
            y *= _KM_TO_AU
            z *= _KM_TO_AU
    elif note2 == "v":
        x, y, z = _roving_position(x, y, z)
        x *= _KM_TO_AU
        y *= _KM_TO_AU
        z *= _KM_TO_AU
    else:
        return False

    obs.earth_obs = [x, y, z]
    obs.spacebased = True
    return True


def parse_mpc80_file(filepath: str) -> Dict[str, List[Observation]]:
    """Parse an MPC 80-column format observation file.

    Groups observations by designation (first 12 characters of each line).
    Satellite/roving second lines (note2 's' / 'v') are applied to the
    preceding observation of the same designation.

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

            if line[14] in ("s", "v"):
                obs_list = tracklets.get(line[0:12])
                if obs_list:
                    _apply_mpc80_second_line(line, obs_list[-1])
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
    from lxml import etree as ET

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

        # Satellite / roving observer position (sys + pos1/pos2/pos3)
        def _text(tag):
            el = optical.find(f"{ns}{tag}")
            return el.text.strip() if el is not None and el.text else None

        spacebased, earth_obs = _observer_position(
            _text("sys"), _text("pos1"), _text("pos2"), _text("pos3"))

        return Observation(
            mjd=mjd,
            ra=ra_deg,
            dec=dec_deg,
            mag=vmag,
            band=band,
            obscode=obscode,
            rms_ra=rms_ra,
            rms_dec=rms_dec,
            spacebased=spacebased,
            earth_obs=earth_obs,
        )

    except (ValueError, AttributeError):
        return None


def _as_float(val: str, default: float = 0.0) -> float:
    """Convert a string to float, treating empty string or literal 'None' as default."""
    return float(val) if val and val != "None" else default


def _parse_ades_psv_row(row: Dict[str, str]) -> Optional[Observation]:
    """Parse a single ADES PSV row dict into an Observation."""
    try:
        mjd = _iso_to_mjd(row["obsTime"].strip())
        ra_deg = float(row["ra"])
        dec_deg = float(row["dec"])
        obscode = row["stn"].strip()
        if not obscode:
            return None
        mag = _as_float(row.get("mag", ""))
        band = row.get("band", "V") or "V"
        rms_ra = _as_float(row.get("rmsRA", ""))
        rms_dec = _as_float(row.get("rmsDec", ""))

        vmag = _update_magnitude(band, mag)

        def _field(key):
            val = row.get(key, "").strip()
            return val if val and val != "None" else None

        spacebased, earth_obs = _observer_position(
            _field("sys"), _field("pos1"), _field("pos2"), _field("pos3"))

        return Observation(
            mjd=mjd,
            ra=ra_deg,
            dec=dec_deg,
            mag=vmag,
            band=band,
            obscode=obscode,
            rms_ra=rms_ra,
            rms_dec=rms_dec,
            spacebased=spacebased,
            earth_obs=earth_obs,
        )
    except (ValueError, KeyError):
        return None


def parse_ades_psv(filepath: str) -> Dict[str, List[Observation]]:
    """Parse an ADES PSV (pipe-separated values) observation file.

    Groups observations by tracklet sub-designation, with fallback to
    provID then permID. Observations within each tracklet
    are returned sorted by MJD ascending, as required by the digest2
    scoring engine.

    Args:
        filepath: Path to the ADES PSV file.

    Returns:
        Dict mapping designation string -> list of Observations sorted by MJD.
        Rows that cannot be parsed are skipped silently.
    """

    def _split(line: str) -> List[str]:
        """Split a PSV line on '|', strip whitespace, and drop trailing empty field."""
        parts = [p.strip() for p in line.split("|")]
        if parts and parts[-1] == "":
            parts = parts[:-1]
        return parts

    tracklets: Dict[str, List[Observation]] = {}
    headers: Optional[List[str]] = None

    with open(filepath, "r") as f:
        for raw_line in f:
            line = raw_line.rstrip("\n")
            if line.startswith("#"):
                continue
            # Skip metadata key-value lines (e.g. "! mpcCode G96") but not the
            # column-header line which also starts with "!" in the full ADES spec
            # (e.g. "!Obstype|permID|...").
            if line.startswith("!") and "|" not in line:
                continue
            if line.startswith("!"):
                line = line[1:]  # strip leading "!" from "!Obstype|..." header
            if headers is None:
                headers = _split(line)
                continue
            fields = _split(line)
            if len(fields) != len(headers):
                continue

            row = dict(zip(headers, fields))
            desig = next(
                (v for k in ("trkSub", "provID", "permID")
                 if (v := row.get(k, "")) and v != "None"),
                "unknown",
            )

            obs = _parse_ades_psv_row(row)
            if obs is not None:
                tracklets.setdefault(desig, []).append(obs)

    return {k: sorted(v, key=lambda o: o.mjd) for k, v in tracklets.items()}


def _iso_to_mjd(iso_str: str) -> float:
    """Convert ISO 8601 datetime string to MJD.

    Handles formats like: ``2022-12-25T09:14:20.544Z``

    Unlike :func:`_date_to_mjd`, there is no C-parity constraint here
    because ADES XML parsing is done entirely in Python (the C CLI's
    ``d2ades.c`` is not used by the Python package).

    Uses :func:`datetime.fromisoformat` with :func:`_date_to_mjd` for
    fast conversion (~1 µs) without the astropy dependency (~500 µs).
    """
    # Strip trailing 'Z' for Python 3.8-3.10 compatibility
    # (fromisoformat gained timezone suffix support in 3.11)
    s = iso_str.strip()
    if s.endswith("Z"):
        s = s[:-1]
    dt = datetime.fromisoformat(s)
    day_fraction = (dt.hour + dt.minute / 60.0 + dt.second / 3600.0
                    + dt.microsecond / 3_600_000_000.0)
    return _date_to_mjd(dt.year, dt.month, dt.day + day_fraction / 24.0)
