"""These are not really unit-tests per se.

These are more performance tests for my own edification.

In summary: the caching helps make it ~100x faster to get the same data
"""

from timeit import default_timer as timer

# Third-party imports
# -----------------------------------------
import numpy as np
import pytest
from astropy.time import Time

from wis.kernels import DE430
from wis.obscodes import MPCObsCodes

# Local imports
# -----------------------------------------
from wis.wis import Wis

pytestmark = pytest.mark.integration

# Test Functions
# -----------------------------------------
###     Initial tests suggest 0.3s for 10^4 evaluations


def test_speed_Ground_A() -> None:
    """Test speed of execution of multiple calls to get positions from the ground.

    Here we instantiate a new wis object for each call: this is SLOW.
    """
    # Select some obs-codes
    n_o = 100
    rand_obscodes = np.random.choice(
        list(MPCObsCodes().geocentric_xyz_dict.keys()), n_o
    )

    # Select some dates
    n_t = 100
    JD0 = 2451545.0
    rand_times = JD0 + 100 * np.random.rand(n_t)
    times = Time(rand_times, format="jd", scale="tdb")

    # Query each obscode for all times
    start_time = timer()
    for obscode in rand_obscodes:
        with Wis(kernels=DE430) as W:
            obs_helio_equ_AU, _ltts = W.get_obs_helio_equ_AU(
                obscode, times, fallback_to_geo=False
            )
        assert obs_helio_equ_AU.shape == (n_t, 3)

    elapsed = timer() - start_time
    print("Elapsed time for test_speed_Ground_A:", elapsed)
    assert (
        elapsed > 1.0
    ), f"Elapsed time expected to be LONG (because of deliberately inefficient code): {elapsed:.3f}s"


def test_speed_Ground_B() -> None:
    """Test speed of execution of multiple calls to get positions from the ground.

    Here we instantiate a single wis object, and then make repeated calls to get_obs_helio_equ_AU.
    This should be FAST.
    """
    # Select some obs-codes
    n_o = 30
    rand_obscodes = np.random.choice(
        list(MPCObsCodes().geocentric_xyz_dict.keys()), n_o
    )

    # Select some dates
    n_t = 100
    JD0 = 2451545.0
    rand_times = JD0 + 100 * np.random.rand(n_t)
    times = Time(rand_times, format="jd", scale="tdb")

    # Instantiate outside of timing loop
    with Wis(kernels=DE430) as W:
        # Query each obscode for all times
        start_time = timer()
        for obscode in rand_obscodes:
            obs_helio_equ_AU, _ltts = W.get_obs_helio_equ_AU(
                obscode, times, fallback_to_geo=False
            )
            assert obs_helio_equ_AU.shape == (n_t, 3)

    elapsed = timer() - start_time
    print("Elapsed time for test_speed_Ground_B:", elapsed)
    assert (
        elapsed < 1.0
    ), f"Elapsed time expected to be SHORT (no declaration of W inside loop): {elapsed:.3f}s"


def test_speed_Ground_C() -> None:
    """Test speed of execution of multiple calls when we use caching.

    FASTER YET!
    """
    # Select some obs-codes
    n_o = 3
    rand_obscodes = np.random.choice(
        list(MPCObsCodes().geocentric_xyz_dict.keys()), n_o
    )

    # Select some dates
    n_t = 10000
    JD0 = 2451545.0
    rand_times = JD0 + 100 * np.random.rand(n_t)
    times = Time(rand_times, format="jd", scale="tdb")

    # Instantiate outside of timing loop
    with Wis(kernels=DE430) as W:
        # Query each obscode for all times
        start_time = timer()
        for obscode in rand_obscodes:
            obs_helio_equ_AU, _ltts = W.get_obs_helio_equ_AU(
                obscode, times, fallback_to_geo=False
            )
            assert obs_helio_equ_AU.shape == (n_t, 3)
        elapsed_init = timer() - start_time

        # Query again, and this time we expect to see the effects of caching
        start_time = timer()
        for obscode in rand_obscodes:
            obs_helio_equ_AU, _ltts = W.get_obs_helio_equ_AU(
                obscode, times, fallback_to_geo=False
            )
            assert obs_helio_equ_AU.shape == (n_t, 3)
        elapsed_cached = timer() - start_time

    ratio = elapsed_init / elapsed_cached if elapsed_cached else float("inf")
    print(
        f"Elapsed time for test_speed_Ground_C: {elapsed_init:.3f}s (initial) vs {elapsed_cached:.3f}s (cached) ratio={ratio:.1f}"
    )
    # For three 10000-epoch queries, a hit costs ~3ms (rebuilding the exact-ET
    # key and looking it up) and a miss costs ~0.25s (the SPICE calls run again),
    # a measured ratio of ~0.012x. The 0.05x threshold compares that with the
    # uncached ratio of 1x: 4x above the healthy measurement and 20x below a
    # cache that never stores results and recomputes every call.
    assert (
        elapsed_cached < 0.05 * elapsed_init
    ), f"Expected caching to speed up execution by a factor of 20 or more (ratio={ratio:.1f})"
