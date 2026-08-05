"""Unit tests for the cache key used by `Wis.get_obs_helio_equ_AU`.

`Wis.compute_key` is a plain function of the call arguments, so it can be exercised
directly. That keeps coverage of the key logic in the unit-test run, where the
end-to-end regression tests in `test_wis_ephemeris.py` need kernels and network.
"""

from astropy.time import Time

from wis.wis import Wis


def test_compute_key_distinguishes_time_scales() -> None:
    """A UTC and a TDB Time with the same numeric JD must not share a cache key.

    They are ~69s (~2000km of Earth motion) apart, and `_convert_time` feeds SPICE
    `times.utc.jd`, so the key has to be built from the same quantity.
    """
    jd = 2458337.82915783
    key_utc = Wis.compute_key(None, "F51", Time(jd, format="jd", scale="utc"))
    key_tdb = Wis.compute_key(None, "F51", Time(jd, format="jd", scale="tdb"))
    assert key_utc != key_tdb


def test_compute_key_is_stable_for_equal_inputs() -> None:
    """Separate but equal Time objects must share a cache key (else nothing is cached)."""
    jd = [2458337.82915783, 2458338.82915783]
    key_a = Wis.compute_key(None, "F51", Time(jd, format="jd", scale="tdb"))
    key_b = Wis.compute_key(None, "F51", Time(jd, format="jd", scale="tdb"))
    assert key_a == key_b


def test_compute_key_distinguishes_flags() -> None:
    """`fallback_to_geo` / `return_velocity` must key the same whether positional or keyword."""
    times = Time([2458337.82915783], format="jd", scale="tdb")

    default = Wis.compute_key(None, "ZZZ", times)
    positional = Wis.compute_key(None, "ZZZ", times, True)
    keyword = Wis.compute_key(None, "ZZZ", times, fallback_to_geo=True)

    assert default != positional
    assert positional == keyword
