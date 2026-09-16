"""Unit tests for the cache keys used by `Wis.get_obs_helio_equ_AU` and `get_bary_wrt_helio`.

`Wis.compute_obs_helio_equ_AU_key` and `Wis.compute_bary_wrt_helio_key` are plain
functions of the call arguments, so they can be exercised directly. That keeps
coverage of the key logic in the unit-test run, where the end-to-end regression
tests in `test_wis_ephemeris.py` need kernels and network.
"""

from collections.abc import Callable
from functools import partial

import numpy as np
import pytest
import spiceypy as sp
from astropy.time import Time
from cachetools import LRUCache

from wis.wis import Wis

KEY_FUNC_CASES = [
    pytest.param(
        partial(Wis.compute_obs_helio_equ_AU_key, None, "F51"),
        id="get_obs_helio_equ_AU",
    ),
    pytest.param(
        partial(Wis.compute_bary_wrt_helio_key, None),
        id="get_bary_wrt_helio",
    ),
]


def _fake_spkezr(
    target: str, epochs: np.ndarray, frame: str, abcorr: str, observer: str
) -> tuple[list[list[float]], list[float]]:
    """Minimal spkezr stub: one (x, y, z, vx, vy, vz) state and ltt per epoch."""
    return ([[1.0, 2.0, 3.0, 4.0, 5.0, 6.0]] * len(epochs), [0.0] * len(epochs))


@pytest.fixture
def bare_wis(monkeypatch: pytest.MonkeyPatch) -> Wis:
    """A Wis instance with no `__init__`, kernels, or network; SPICE calls are stubbed."""
    instance = Wis.__new__(Wis)
    instance.cache_get_obs_helio_equ_AU = LRUCache(maxsize=1024)
    instance.cache_get_bary_wrt_helio = LRUCache(maxsize=1024)
    instance.geocentric_xyz_dict = {"F51": np.array([0.1, 0.2, 0.3])}
    instance._entered = True
    monkeypatch.setattr(instance, "_has_ground_kernel", lambda: True)
    monkeypatch.setattr(instance, "_has_satellite_kernel", lambda obscode: False)
    # `_convert_time` calls utc2et, which needs leapsecond kernels; stub it out.
    monkeypatch.setattr(sp, "utc2et", lambda _: 0.0)
    monkeypatch.setattr(sp, "pxform", lambda *args: np.eye(3))
    monkeypatch.setattr(sp, "spkpos", lambda *args: ([[1.0, 2.0, 3.0]], [0.0]))
    monkeypatch.setattr(sp, "spkezr", _fake_spkezr)
    return instance


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

    default = Wis.compute_obs_helio_equ_AU_key(None, "ZZZ", times)
    positional = Wis.compute_obs_helio_equ_AU_key(None, "ZZZ", times, True)
    keyword = Wis.compute_obs_helio_equ_AU_key(None, "ZZZ", times, fallback_to_geo=True)

    assert default != positional
    assert positional == keyword


def test_get_bary_wrt_helio_caches_spice_call(
    bare_wis: Wis,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Two identical calls must reach SPICE once and reuse the cached arrays."""
    calls: list[np.ndarray] = []

    def counting_spkezr(
        target: str, epochs: np.ndarray, frame: str, abcorr: str, observer: str
    ) -> tuple[list[list[float]], list[float]]:
        calls.append(epochs)
        return _fake_spkezr(target, epochs, frame, abcorr, observer)

    monkeypatch.setattr(sp, "spkezr", counting_spkezr)

    times = Time([2458337.82915783], format="jd", scale="utc")
    first = bare_wis.get_bary_wrt_helio(times)
    second = bare_wis.get_bary_wrt_helio(times)

    assert len(calls) == 1
    assert first[0][0, 0] == second[0][0, 0]


def test_cached_results_are_read_only(bare_wis: Wis) -> None:
    """The cached arrays are shared between callers, so they are returned read-only."""
    times = Time([2458337.82915783], format="jd", scale="tdb")

    obs_result = bare_wis.get_obs_helio_equ_AU("F51", times)
    assert obs_result is not None
    for array in (*obs_result, *bare_wis.get_bary_wrt_helio(times)):
        assert not array.flags.writeable


def test_in_place_mutation_of_cached_results_raises(bare_wis: Wis) -> None:
    """A caller cannot corrupt the shared cache entry by mutating a returned array."""
    times = Time([2458337.82915783], format="jd", scale="tdb")

    obs_posns, _ = bare_wis.get_obs_helio_equ_AU("F51", times)
    bary_posns, _, _ = bare_wis.get_bary_wrt_helio(times)

    with pytest.raises(ValueError):
        obs_posns[0, 0] = 0.0
    with pytest.raises(ValueError):
        bary_posns[0, 0] = 0.0
