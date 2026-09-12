"""Unit tests for the cache keys used by `Wis.get_obs_helio_equ_AU` and `get_bary_wrt_helio`.

`Wis.compute_key` and `Wis.compute_bary_wrt_helio_key` are plain functions of the
call arguments, so they can be exercised directly. That keeps coverage of the key
logic in the unit-test run, where the end-to-end regression tests in
`test_wis_ephemeris.py` need kernels and network.
"""

from collections.abc import Callable

import numpy as np
import pytest
import spiceypy as sp
from astropy.time import Time
from cachetools import LRUCache

from wis.wis import Wis


def _obs_helio_key(times: Time) -> tuple:
    return Wis.compute_key(None, "F51", times)


def _bary_wrt_helio_key(times: Time) -> tuple:
    return Wis.compute_bary_wrt_helio_key(None, times)


KEY_FUNC_CASES = [
    pytest.param(_obs_helio_key, id="get_obs_helio_equ_AU"),
    pytest.param(_bary_wrt_helio_key, id="get_bary_wrt_helio"),
]


@pytest.mark.parametrize("key_func", KEY_FUNC_CASES)
def test_key_distinguishes_time_scales(key_func: Callable[[Time], tuple]) -> None:
    """A UTC and a TDB Time with the same numeric JD must not share a cache key.

    They are ~69s (~2000km of Earth motion) apart, and `_convert_time` feeds SPICE
    `times.utc.jd`, so the key has to be built from the same quantity.
    """
    jd = 2458337.82915783
    key_utc = key_func(Time(jd, format="jd", scale="utc"))
    key_tdb = key_func(Time(jd, format="jd", scale="tdb"))
    assert key_utc != key_tdb


@pytest.mark.parametrize("key_func", KEY_FUNC_CASES)
def test_key_is_stable_for_equal_inputs(key_func: Callable[[Time], tuple]) -> None:
    """Separate but equal Time objects must share a cache key (else nothing is cached)."""
    jd = [2458337.82915783, 2458338.82915783]
    key_a = key_func(Time(jd, format="jd", scale="tdb"))
    key_b = key_func(Time(jd, format="jd", scale="tdb"))
    assert key_a == key_b


@pytest.mark.parametrize("key_func", KEY_FUNC_CASES)
def test_key_distinguishes_time_values(key_func: Callable[[Time], tuple]) -> None:
    """A different time value must not share a cache key."""
    key_a = key_func(Time(2458337.82915783, format="jd", scale="tdb"))
    key_b = key_func(Time(2458338.82915783, format="jd", scale="tdb"))
    assert key_a != key_b


def test_obs_helio_key_distinguishes_flags() -> None:
    """`fallback_to_geo` / `return_velocity` must key the same whether positional or keyword."""
    times = Time([2458337.82915783], format="jd", scale="tdb")

    default = Wis.compute_key(None, "ZZZ", times)
    positional = Wis.compute_key(None, "ZZZ", times, True)
    keyword = Wis.compute_key(None, "ZZZ", times, fallback_to_geo=True)

    assert default != positional
    assert positional == keyword


def test_get_bary_wrt_helio_caches_spice_call(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Two identical calls must reach SPICE once and reuse the cached arrays."""
    calls: list[np.ndarray] = []

    def fake_spkezr(
        target: str, epochs: np.ndarray, frame: str, abcorr: str, observer: str
    ) -> tuple[list[list[float]], list[float]]:
        calls.append(epochs)
        return ([[1.0, 2.0, 3.0, 4.0, 5.0, 6.0]] * len(epochs), [0.0] * len(epochs))

    monkeypatch.setattr(sp, "spkezr", fake_spkezr)
    # `_convert_time` calls utc2et, which needs leapsecond kernels; stub it out.
    monkeypatch.setattr(sp, "utc2et", lambda _: 0.0)

    instance = Wis.__new__(Wis)  # <- no __init__, so no kernels or network
    instance.cache_get_bary_wrt_helio = LRUCache(maxsize=1024)
    monkeypatch.setattr(instance, "_has_ground_kernel", lambda: True)
    instance._entered = True

    times = Time([2458337.82915783], format="jd", scale="utc")
    first = instance.get_bary_wrt_helio(times)
    second = instance.get_bary_wrt_helio(times)

    assert len(calls) == 1
    assert first[0][0, 0] == second[0][0, 0]
