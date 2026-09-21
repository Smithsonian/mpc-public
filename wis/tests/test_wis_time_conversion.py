"""Unit tests for `Wis._convert_time`.

`_convert_time` is pure time handling: these tests call it on a bare `Wis`
instance and need no ephemeris kernels, only the leap-seconds kernel that SPICE's
own string parsers require.
"""

import re
from collections.abc import Iterator
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pytest
import spiceypy as sp
from astropy.time import Time

from wis.wis import Wis

LSK = Path(__file__).parent.parent / "test_data" / "latest_leapseconds.tls"

_LEAP_SECOND_ENTRY = re.compile(r"@(\d{4})-([A-Z]{3})-(\d{1,2})")


def _leap_second_dates() -> list[str]:
    """The UTC dates that held a leap second, read from the leap-seconds kernel.

    `DELTET/DELTA_AT` lists the date on which TAI-UTC steps up, so the leap second
    itself falls on the day before each entry. The first entry fixes the 1972
    baseline rather than adding a second.
    """
    entries = _LEAP_SECOND_ENTRY.findall(LSK.read_text())[1:]
    return [
        (
            datetime.strptime(f"{year}-{month}-{day}", "%Y-%b-%d") - timedelta(days=1)
        ).strftime("%Y-%m-%d")
        for year, month, day in entries
    ]


# The UTC days that are 86401 s long: only on those days can the epoch written by
# astropy and the epoch read by SPICE disagree.
LEAP_SECOND_DATES = _leap_second_dates()

# Tolerance for an epoch inside a leap-second day, where a UTC day is 86401 s long
# and the two libraries can disagree by up to a second. Three orders of magnitude
# below that, and well above the TDB-TT difference bounded by TDB_TT_TOL_S.
LEAP_DAY_TOL_S = 1e-3

# Tolerance for epochs that are not inside a leap-second day, where the only
# difference left is how the two libraries model TDB-TT. The models and their
# accuracies are cited in the test below; measured, they differ by at most
# 3.6e-5 s over 1972-2030.
TDB_TT_TOL_S = 1e-4

FIRST_EPOCH, LAST_EPOCH = "1972-01-01", "2030-01-01"


@pytest.fixture(scope="module")
def leapseconds() -> Iterator[None]:
    """Load the leap-seconds kernel needed by `str2et`."""
    sp.furnsh(str(LSK))
    yield
    sp.unload(str(LSK))


def _convert(times: Time) -> np.ndarray:
    """Call `_convert_time` without instantiating a `Wis` (which needs kernels)."""
    return np.array(object.__new__(Wis)._convert_time(times))


def _spice_et(times: Time) -> np.ndarray:
    """SPICE's own ET for the same epochs, parsed from UTC calendar strings.

    `isot` is given nanosecond precision because its default millisecond
    precision would quantize the comparison to ~5e-4 s.
    """
    utc = times.utc.copy()
    utc.precision = 9
    return np.array(sp.str2et(np.atleast_1d(utc.isot)))


def _utc_dates(times: Time) -> list[str]:
    """The UTC calendar dates of `times`, as `YYYY-MM-DD` strings."""
    return [s[:10] for s in np.atleast_1d(times.utc.isot)]


@pytest.mark.parametrize("date", LEAP_SECOND_DATES)
@pytest.mark.parametrize("time_of_day", ["00:00:01", "12:00:00", "23:59:59"])
def test_leap_second_epochs_match_spice(
    leapseconds: None, date: str, time_of_day: str
) -> None:
    """Epochs inside a leap-second day must match SPICE to well under a second.

    A leap-second day lasts 86401 s, so a Julian date written for it by astropy and
    read back by SPICE can land a second away. SPICE's parsing of the UTC calendar
    string is the reference for what the epoch is.
    """
    times = Time(f"{date}T{time_of_day}", scale="utc")
    error = _convert(times)[0] - _spice_et(times)[0]
    assert abs(error) < LEAP_DAY_TOL_S, (
        f"{date}T{time_of_day}: epoch is off by {error:+.6f} s"
    )


def test_ordinary_epochs_differ_only_by_the_tdb_model(leapseconds: None) -> None:
    """Away from leap seconds, nothing but the TDB-TT model may differ.

    Epochs on leap-second days are excluded, so the leap tables agree and the only
    difference left is how each library models TDB-TT, a periodic term of about
    1.7 ms peak to peak. ERFA uses the full Fairhead & Bretagnon (1990) series
    (https://pyerfa.readthedocs.io/en/stable/api/erfa.dtdb.html), rated at +/- 3 ns
    over 1950-2050; the toolkit's model is the truncated TDB - TT = K*sin(E) given
    in its time documentation
    (https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/time.html), with the
    DELTET constants in the leap-seconds kernel, rated at about 3e-5 s. The
    tolerance is that model difference, orders of magnitude below the error a
    leap-second mistake would produce.
    """
    times = Time(
        np.linspace(
            Time(FIRST_EPOCH, scale="utc").jd, Time(LAST_EPOCH, scale="utc").jd, 2000
        ),
        format="jd",
        scale="utc",
    )
    ordinary = ~np.isin(_utc_dates(times), LEAP_SECOND_DATES)
    assert ordinary.sum() > 1900, "expected leap-second days to be a small sample"

    difference = _convert(times[ordinary]) - _spice_et(times[ordinary])
    worst = int(np.abs(difference).argmax())
    assert np.abs(difference).max() < TDB_TT_TOL_S, (
        f"worst epoch {times[ordinary][worst].utc.isot}: "
        f"off by {difference[worst]:+.3e} s"
    )


def test_convert_time_does_not_use_spice_string_parsing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """No per-epoch SPICE string parse: the epoch comes from astropy's TDB."""

    def _unexpected(*args: object, **kwargs: object) -> float:
        raise AssertionError("_convert_time called a SPICE string parser")

    monkeypatch.setattr(sp, "utc2et", _unexpected)
    monkeypatch.setattr(sp, "str2et", _unexpected)

    times = Time("2025-06-15T03:00:00", scale="utc")
    assert _convert(times).shape == (1,)


def test_convert_time_returns_tuple_for_scalar_input() -> None:
    """Scalar input yields a 1-element tuple, which callers hash for cache keys."""
    epochs = object.__new__(Wis)._convert_time(Time("2025-06-15T03:00:00", scale="utc"))
    assert isinstance(epochs, tuple)
    assert len(epochs) == 1
