"""Unit tests for `Wis._convert_time`.

`_convert_time` is pure time handling: these tests call it on a bare `Wis`
instance and need no ephemeris kernels, only the leap-seconds kernel that SPICE's
own string parsers require.
"""

from collections.abc import Iterator
from pathlib import Path

import numpy as np
import pytest
import spiceypy as sp
from astropy.time import Time

from wis.wis import Wis

LSK = Path(__file__).parent.parent / "test_data" / "latest_leapseconds.tls"

# The UTC days that held a leap second, i.e. the only UTC days that are 86401 s
# long. On those days the UTC JD written by astropy and the UTC JD read by SPICE
# disagree; on every other day they coincide.
LEAP_SECOND_DATES = [
    "1972-06-30",
    "1972-12-31",
    "1973-12-31",
    "1974-12-31",
    "1975-12-31",
    "1976-12-31",
    "1977-12-31",
    "1978-12-31",
    "1979-12-31",
    "1981-06-30",
    "1982-06-30",
    "1983-06-30",
    "1985-06-30",
    "1987-12-31",
    "1989-12-31",
    "1990-12-31",
    "1992-06-30",
    "1993-06-30",
    "1994-06-30",
    "1995-12-31",
    "1997-06-30",
    "1998-12-31",
    "2005-12-31",
    "2008-12-31",
    "2012-06-30",
    "2015-06-30",
    "2016-12-31",
]

# Tolerance for epochs inside a leap-second day: three orders of magnitude below
# the ~1 s error the UTC JD string produces there, and thirty above the TDB-TT
# model difference between the two libraries.
LEAP_DAY_TOL_S = 1e-3

# Tolerance for epochs away from leap seconds. There the leap tables agree, so the
# only difference is the TDB-TT model: ERFA's full Fairhead & Bretagnon series
# against the truncated K*sin(E) series in the leap-seconds kernel. ERFA rates its
# own model at +/- 3 ns over 1950-2050, the kernel rates its own at about 3e-5 s,
# and the two differ by at most 3.6e-5 s over the range tested below.
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

    The 86401-second day is the only place the two UTC Julian date conventions
    differ, so this is where a string round-trip shows up. SPICE parses the UTC
    calendar string directly, which is the reference for what the epoch is.
    """
    times = Time(f"{date}T{time_of_day}", scale="utc")
    error = _convert(times)[0] - _spice_et(times)[0]
    assert abs(error) < LEAP_DAY_TOL_S, (
        f"{date}T{time_of_day}: epoch is off by {error:+.6f} s"
    )


def test_ordinary_epochs_differ_only_by_the_tdb_model(leapseconds: None) -> None:
    """Away from leap seconds, nothing but the TDB-TT model may differ.

    Epochs on leap-second days are excluded, so the UTC-noon and leap-second
    questions are out of the way: the leap tables agree, and the only remaining
    difference between the two libraries is how each realizes TDB from TT --
    ERFA's full Fairhead & Bretagnon series against the truncated `K*sin(E)`
    series in the leap-seconds kernel.

    The tolerance is the width of that model difference, three orders of
    magnitude below the ~1 s error a leap-second mistake would produce.
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
