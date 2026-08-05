"""Integration tests for wis ephemeris kernel behavior."""

import numpy as np
import pytest
import spiceypy as sp
from astropy.time import Time
from jplephem.spk import (
    SPK,
)  # <- For comparison with spiceypy: *NOT* used in the actual code

from wis.kernel_instances_ground import DE430, DE440, GROUND
from wis.kernels import TESS
from wis.wis import Wis

pytestmark = pytest.mark.integration

# -------------------------------------------------------------------
# Tests of basic functionalities
# -------------------------------------------------------------------


np.set_printoptions(precision=16)

# NB: no cache-clearing fixture is needed -- the get_obs_helio_equ_AU cache lives on
# the Wis instance, so it is discarded along with the instance at the end of each test.


def test_change_actually_occurs_1() -> None:
    """Test that the loaded kernels differ when different ephemeris kernels are loaded."""
    # Get the loaded kernels for each DE
    loaded_kernels = {}  # <- Dictionary to store the loaded kernels
    for kernel, name in [(DE430, "DE430"), (DE440, "DE440")]:
        with Wis(kernels=kernel) as W:
            loaded_kernels[name] = [
                sp.kdata(n, "ALL")[0] for n in range(sp.ktotal("ALL"))
            ]  # <- Get loaded kernels
            W.cache_get_obs_helio_equ_AU.clear()  # <- Clear cache
            sp.kclear()  # <- Clear the kernels from memory
            assert (
                sp.ktotal("ALL") == 0
            ), "Kernels not cleared"  # <- check that there are no kernels loaded

    # Check that the kernels are DIFFERENT
    keys = list(loaded_kernels.keys())
    for i in range(len(keys) - 1):
        assert (
            loaded_kernels[keys[i]] != loaded_kernels[keys[i + 1]]
        ), "Loaded kernels are not different"


def test_change_actually_occurs_2() -> None:
    """Test that a direct calculation of the location of Earth (399) changes when different ephemeris kernels are loaded.

    NB: From `test_change_actually_occurs_1` above, we have established that the loaded DE4** file changes.
    """
    # Get the loaded kernels for each DE
    pos_earth = (
        {}
    )  # <- Dictionary to store location of Earth under different DE*** models
    for kernel, name in [(DE430, "DE430"), (DE440, "DE440")]:
        with Wis(kernels=kernel) as W:  # <- This will cause the kernels to be loaded
            # Explicitly calculate the position of Earth (399) via a direct spicepy call
            # I.e. I am deliberately not testing `wis.py` positions at this point
            # N.B test_wis_Wis.py::test_Satellite_C ...
            # times=[2458337.82915783 2458338.82915783]
            # epochs_tuple=(586900439.2365652, 586986839.2365797)
            epochs_tuple = (586900439.2365652, 586986839.2365797)
            pos_earth[name], _lt = sp.spkpos(
                "399", np.array(epochs_tuple), "J2000", "NONE", "Sun"
            )

            # Do thorough clean-up
            W.cache_get_obs_helio_equ_AU.clear()  # <- Clear cache
            sp.kclear()  # <- Clear the kernels from memory
            assert (
                sp.ktotal("ALL") == 0
            ), "Kernels not cleared"  # <- check that there are no kernels loaded

    # Check that the positions of Earth are different-but-close for all DEs
    # NB: At the individual component level we are expecting to see things like ...
    #     X_DE430=108166309.26191282
    #     X_DE440=108166309.14543432
    # I.e. differences around the km-or-less level
    keys = list(pos_earth.keys())
    for i in range(len(keys) - 1):  # <- Looping over comparison DEs
        DE_i = pos_earth[keys[i]]
        DE_ip1 = pos_earth[keys[i + 1]]
        for j in range(len(DE_i)):  # <- Looping over sets of positions (sets of epochs)
            xyz_i = DE_i[j]
            xyz_ip1 = DE_ip1[j]
            for k in range(len(xyz_i)):  # <- Looping over x / y / z
                assert (
                    xyz_i[k] != xyz_ip1[k]
                ), f"Positions are not different: xyz_i[k]={xyz_i[k]}, xyz_ip1[k]={xyz_ip1[k]}"
                assert np.allclose(
                    xyz_i[k], xyz_ip1[k], rtol=1e-03, atol=1e-03
                ), "Positions not close"


def test_obs_geo_equ_ephem_change() -> None:
    """Test observatory position calculation against Horizons (km).

    The Horizons query below is returning the position of the observatory w.r.t. the center of the Earth
    I.e. this is a GEOCENTRIC position, not a heliocentric one.

    This means that we do **NOT** expect the position to change as a function of the ephemeris
    """
    # Time & Obscode of interest
    times = Time([2458337.82915783, 2458338.82915783], format="jd", scale="tdb")
    obscode = "F51"

    # Get positions under different DEs
    results = {}
    for kernel, name in [(DE430, "DE430"), (DE440, "DE440")]:
        # Instantiate & call the get_obs_helio_equ_AU method (which populates `obs_geo_equ` )
        with Wis(kernels=kernel) as W:
            W.get_obs_helio_equ_AU(obscode, times)

            # # NB: In `test_wis_Wis:test_Ground_geocentric` we test that the returned positions as expected:
            # #X = 3.357062612610595E+03 Y =-4.938472797753120E+03 Z =-2.242238952821062E+03
            # #X = 3.441514318240966E+03 Y =-4.879997205156549E+03 Z =-2.242236596724388E+03
            # assert np.allclose(W.obs_geo_equ , expectedPosns, rtol=1e-06, atol=1e+02), \
            #     ' Not close enough to expected values: returned=[%r], expected=[%r]' % (W.obs_vec_rot , expectedPosns)

            # Store the value of `obs_geo_equ`
            results[name] = W.obs_geo_equ

            # Forcibly clear the cache
            W.cache_get_obs_helio_equ_AU.clear()
            sp.kclear()  # <- Clear the kernels from memory
            assert (
                sp.ktotal("ALL") == 0
            ), "Kernels not cleared"  # <- check that there are no kernels loaded

    # Check that the positions are the same for all DEs
    keys = list(results.keys())
    for i in range(len(keys) - 1):
        assert np.allclose(
            results[keys[i]], results[keys[i + 1]], rtol=1e-06, atol=1e-06
        ), f" Not close enough to expected values: returned=[{results[keys[i]]!r}], expected=[{results[keys[i + 1]]!r}]"


def test_obs_helio_equ_AU_ephem_change() -> None:
    """Compare obs_helio_equ_AU between models.

    These are heliocentric positions, so we expect them to CHANGE as a function of the ephemeris.
    """
    np.set_printoptions(precision=16)

    # Time & Obscode of interest
    times = Time([2458337.82915783, 2458338.82915783], format="jd", scale="tdb")
    obscode = "F51"

    # Get positions under different DEs
    results = {}
    for kernel, name in [(DE430, "DE430"), (DE440, "DE440")]:
        with Wis(kernels=kernel) as W:  # <- Instantiate Wis
            W.get_obs_helio_equ_AU(
                obscode, times
            )  # <- Call the get_obs_helio_equ_AU method
            results[name] = (
                W.obs_helio_equ_AU
            )  # <- Store the value of ***`obs_helio_equ_AU`***

            W.cache_get_obs_helio_equ_AU.clear()  # <- Forcibly clear the cache
            sp.kclear()  # <- Clear the kernels from memory
            assert (
                sp.ktotal("ALL") == 0
            ), "Kernels not cleared"  # <- check that there are no kernels loaded

    # Check that the positions of F51 are different-but-close for all DEs
    # NB: At the individual component level we are expecting to see things like ...
    #     X_DE430=0.7111605937322192
    #     X_DE440=0.7111605929403113
    # I.e. differences around the km-or-less level
    # (Previously this loop iterated over `pos_earth`, which was never populated — bug fix)
    keys = list(results.keys())
    for i in range(len(keys) - 1):  # <- Looping over comparison DEs
        res_i = results[keys[i]]  # shape (N_times, 3) in AU
        res_ip1 = results[keys[i + 1]]
        for j in range(
            len(res_i)
        ):  # <- Looping over sets of positions (sets of epochs)
            xyz_i = res_i[j]
            xyz_ip1 = res_ip1[j]
            for k in range(len(xyz_i)):  # <- Looping over x / y / z
                assert (
                    xyz_i[k] != xyz_ip1[k]
                ), f"Positions are not different: xyz_i[k]={xyz_i[k]}, xyz_ip1[k]={xyz_ip1[k]}"
                assert np.allclose(
                    xyz_i[k], xyz_ip1[k], rtol=1e-03, atol=1e-03
                ), "Positions not close"


# -------------------------------------------------------------------
# Tests of get_bary_wrt_helio
# -------------------------------------------------------------------


def test_get_bary_wrt_helio() -> None:
    """Test that get_bary_wrt_helio returns the same as the jplephem package.

    jplephem.SPK.open(os.path.join(DATA_PATH, 'de440.bsp'))[0,10].compute_and_differentiate().

    While function as a test, this is also a way for MJP to double-check his
    understanding of various pieces of the spiceypy code ...
    """
    # Time of interest
    jd_tdb = [2458337.82915783]  # , 2458338.82915783
    times = Time(jd_tdb, format="jd", scale="tdb")

    # Get the position of the barycenter w.r.t. the heliocenter at the specified times
    with Wis(kernels=DE430) as W:
        # Execute the get_bary_wrt_helio method that we want to test
        posns, _vels, _ltts = W.get_bary_wrt_helio(times)

        # Explicitly execute various spiceypy calls to get the same data
        # ---------------------------------------------------------------
        # (using the kernels that have been loaded by Wis)
        # (1) spkezr:
        #     Return the state (position and velocity) of a target body ['10'==Sun/Heliocenter] relative to an observing body ['0'==SSB] , optionally corrected for light time (planetary aberration) and stellar aberration.
        result_spkezr = sp.spkezr(
            "10", np.array(W._convert_time(times)), W.frame, W.abcorr, "0"
        )
        p0_spkezr = result_spkezr[0][0][:3]

        # (2) spkpos:
        # Return the position of a target body ['10'==Sun/Heliocenter] relative to an observing body ['0'==SSB], optionally corrected for light time (planetary aberration) and stellar aberration.
        result_spkpos = sp.spkpos(
            "10", np.array(W._convert_time(times)), W.frame, W.abcorr, "0"
        )
        p0_spkpos = result_spkpos[0][0]

        # (3) spkssb:
        # Return the state (position and velocity) of a target body relative to the solar system barycenter.
        et = sp.str2et("JD " + str(times.utc.jd[0]))
        result_spkssb = sp.spkssb(10, et, W.frame)
        p0_spkssb = result_spkssb[:3]

        # Check that the results from the various spiceypy calls are the same
        # - This is *NOT* checking the functioning of wis.py
        # - It is simply checking that MJP understands the various spiceypy calls
        assert np.allclose(
            p0_spkezr, p0_spkpos, rtol=1e-12, atol=1e-12
        ), "p0_spkezr != p0_spkpos"
        assert np.allclose(
            p0_spkezr, p0_spkssb, rtol=1e-12, atol=1e-12
        ), "p0_spkezr != p0_spkssb"

        # Check that `get_bary_wrt_helio` returns (scaled) versions of the spiceypy results.
        # get_bary_wrt_helio now calls spkezr("0",...,"10") — target=SSB, observer=Sun —
        # returning r_ssb - r_sun, i.e. the negative of p0_spkpos (which is r_sun - r_ssb).
        # NB: the comparison is converted from km to AU.
        assert np.allclose(
            posns[0], -W._convert_posn(p0_spkpos), rtol=1e-12, atol=1e-12
        ), "posns[0] != -p0_spkpos"

        # Forcibly clear the cache
        W.cache_get_obs_helio_equ_AU.clear()
        sp.kclear()
        assert sp.ktotal("ALL") == 0, "Kernels not cleared"

        # Get the posns & vels from jplephem
        de_filepath = next(
            _ for _ in GROUND["DE430"].kernel_filepath_map if ".bsp" in _
        )
        p, _v = SPK.open(de_filepath)[0, 10].compute_and_differentiate(times.utc.jd[0])

        # Check that the results from jplephem are CLOSE to those from spiceypy
        # (I do not understand why they are not identical)
        assert np.allclose(p0_spkpos, p, rtol=1e-04, atol=1e-04), "p0_spkpos[0] != p"


def test_get_bary_wrt_helio_shape() -> None:
    """Test the shape of the returned arrays as a function of the input time-arrays ..."""
    with Wis(kernels=DE430) as W:
        jd_tdb = [2458337.82915783]
        times = Time(jd_tdb, format="jd", scale="tdb")
        posns, _vels, _ltts = W.get_bary_wrt_helio(times)
        assert posns.shape == (1, 3), f"posns.shape={posns.shape}"

        jd_tdb = [2458337.82915783, 2458338.82915783]
        times = Time(jd_tdb, format="jd", scale="tdb")
        posns, _vels, _ltts = W.get_bary_wrt_helio(times)
        assert posns.shape == (2, 3), f"posns.shape={posns.shape}"

        jd_tdb = 2458337.82915783
        times = Time(jd_tdb, format="jd", scale="tdb")
        posns, _vels, _ltts = W.get_bary_wrt_helio(times)
        assert posns.shape == (1, 3), f"posns.shape={posns.shape}"


# -------------------------------------------------------------------
# Tests of kernel selection API
# -------------------------------------------------------------------


def test_explicit_kernel_selection() -> None:
    """Test that explicit kernel selection works correctly."""
    # Test with DE430 kernel
    with Wis(kernels=DE430) as W:
        assert len(W.loaded_kernels) == 1
        assert W.loaded_kernels[0].name == "DE430"
        assert W._has_ground_kernel()
        assert not W._has_satellite_kernel("C57")

    # Test with DE440 kernel
    with Wis(kernels=DE440) as W:
        assert len(W.loaded_kernels) == 1
        assert W.loaded_kernels[0].name == "DE440"
        assert W._has_ground_kernel()

    # Test with list of kernels
    with Wis(kernels=[DE430, TESS]) as W:
        assert len(W.loaded_kernels) == 2
        assert W._has_ground_kernel()
        assert W._has_satellite_kernel("C57")


def test_kernel_validation() -> None:
    """Test that appropriate errors are raised for invalid kernel configurations."""
    from astropy.time import Time

    times = Time([2458337.82915783], format="jd", scale="tdb")

    # A ground kernel is always required; instantiating with only a satellite
    # kernel should raise ValueError (not silently succeed)
    with pytest.raises(ValueError, match="No ground kernel loaded"), Wis(
        kernels=TESS
    ) as W:
        pass

    # Trying to calculate satellite position without that satellite kernel should
    # return None (logged as an error but not raised)
    with Wis(kernels=DE430) as W:
        result = W.get_obs_helio_equ_AU("C57", times)
        assert result is None, "Should return None when satellite kernel not loaded"


# -------------------------------------------------------------------
# Tests of cache-key handling and return_velocity
# -------------------------------------------------------------------


def test_cache_key_positional_fallback_no_collision() -> None:
    """Regression test for compute_key.

    `fallback_to_geo` passed positionally must produce a different cache key
    than the default (False), otherwise the cached `None` from a
    fallback_to_geo=False call wrongly satisfies a later fallback_to_geo=True
    call for the same unknown obscode. Also covers scalar-time inputs, which
    previously crashed compute_key's `tuple(times.jd)`.
    """
    times = Time([2458337.82915783, 2458338.82915783], format="jd", scale="tdb")
    unknown = "ZZZ"  # length-3, but not a real obscode

    with Wis(kernels=DE430) as W:
        # Sanity: the obscode really is unknown to this instance
        assert unknown not in W.geocentric_xyz_dict
        assert unknown not in W.known_satellite_obscodes

        # fallback_to_geo=False -> None (cachetools caches the None)
        assert W.get_obs_helio_equ_AU(unknown, times, fallback_to_geo=False) is None

        # fallback_to_geo passed POSITIONALLY as True must hit the geocenter
        # fallback, not the cached None from the call above.
        result = W.get_obs_helio_equ_AU(unknown, times, True)
        assert (
            result is not None
        ), "positional fallback_to_geo=True collided with cached None"
        posns, _ = result
        assert posns.shape == (2, 3)

        # A scalar Time must no longer crash compute_key and returns shape (1, 3)
        scalar_times = Time(2458337.82915783, format="jd", scale="tdb")
        posns_scalar, _ = W.get_obs_helio_equ_AU("F51", scalar_times)
        assert posns_scalar.shape == (1, 3)


def test_cache_key_distinguishes_time_scale() -> None:
    """Regression test for compute_key.

    A UTC and a TDB Time carrying the same numeric JD are ~69s apart, but
    compute_key used to hash the scale-dependent `times.jd` while `_convert_time`
    feeds SPICE the scale-independent `times.utc.jd`. The two calls below therefore
    shared a cache key, and the second silently returned the first's positions.
    """
    jd = 2458337.82915783
    with Wis(kernels=DE430) as W:
        posns_utc, _ = W.get_obs_helio_equ_AU("F51", Time(jd, format="jd", scale="utc"))
        posns_tdb, _ = W.get_obs_helio_equ_AU("F51", Time(jd, format="jd", scale="tdb"))

    # ~69s of Earth orbital motion is ~2e3 km, i.e. ~1.4e-5 AU
    separation_AU = np.linalg.norm(posns_utc[0] - posns_tdb[0])
    assert (
        separation_AU > 1e-6
    ), f"UTC and TDB inputs returned effectively identical positions ({separation_AU} AU)"


def test_cache_not_shared_between_instances() -> None:
    """Regression test: the get_obs_helio_equ_AU cache must not be shared between instances.

    The cache key describes only the call signature (obscode, times, flags) and says
    nothing about which kernels are loaded, so a class-level cache let a DE440
    instance be handed the positions a DE430 instance had already computed for the
    same arguments.

    NB: the context managers are deliberately nested, because that is the only way to
    have two instances alive with populated caches at the same time. Nesting is
    otherwise an anti-pattern here -- the inner __exit__ calls sp.kclear(), which
    unloads the outer instance's kernels too -- so nothing is queried on the outer
    instance after the inner block closes.
    """
    times = Time([2458337.82915783, 2458338.82915783], format="jd", scale="tdb")

    with Wis(kernels=DE430) as W430:
        posns_430, _ = W430.get_obs_helio_equ_AU("F51", times)
        with Wis(kernels=DE440) as W440:
            posns_440, _ = W440.get_obs_helio_equ_AU("F51", times)

    assert not np.array_equal(
        posns_430, posns_440
    ), "DE440 instance was served the DE430 instance's cached positions"
    # ... but the two ephemerides should still agree to well under a km: the measured
    # difference is ~7.9e-10 AU (~0.12km), so 1e-8 AU (~1.5km) leaves ~10x of margin
    assert np.allclose(posns_430, posns_440, rtol=0, atol=1e-8)


def test_ground_return_velocity() -> None:
    """Ground-station return_velocity=True: return structure, shapes, and a finite-difference cross-check of the velocity.

    The cross-check is valid because abcorr='NONE' (no light-time/aberration
    correction), so a central difference of the position recovers the velocity.
    """
    obscode = "F51"
    jd = np.array([2458337.82915783, 2458338.82915783])
    times = Time(jd, format="jd", scale="tdb")

    with Wis(kernels=DE430) as W:
        # Back-compat: the default call still returns a 2-tuple
        default_result = W.get_obs_helio_equ_AU(obscode, times)
        assert len(default_result) == 2

        # return_velocity=True returns a 3-tuple with matching shapes
        posns, vels, _ltts = W.get_obs_helio_equ_AU(
            obscode, times, return_velocity=True
        )
        assert posns.shape == (2, 3)
        assert vels.shape == (2, 3)

        # Central finite difference of the position at each epoch should match
        # the returned velocity [AU/day].
        dt = 60.0 / 86400.0  # 60 s expressed in days
        for jd_i, v_i in zip(jd, vels, strict=False):
            p_plus, _ = W.get_obs_helio_equ_AU(
                obscode, Time(jd_i + dt, format="jd", scale="tdb")
            )
            p_minus, _ = W.get_obs_helio_equ_AU(
                obscode, Time(jd_i - dt, format="jd", scale="tdb")
            )
            v_fd = (p_plus[0] - p_minus[0]) / (2 * dt)
            assert np.allclose(
                v_i, v_fd, rtol=1e-5, atol=1e-9
            ), f"velocity mismatch: returned={v_i}, finite-diff={v_fd}"
