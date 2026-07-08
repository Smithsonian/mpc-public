"""End-to-end Horizons accuracy tests for all known satellite observatories.

Each test queries the heliocentric equatorial position via Wis and compares against
a hardcoded reference value from an explicit JPL Horizons query:
  Center: Sun (10), body center
  Frame: ICRF (REF_PLANE=FRAME, REF_SYSTEM=ICRF)
  Units: AU-D
  Type: GEOMETRIC cartesian states (VEC_CORR=NONE, no aberrations applied)
"""

import numpy as np
import pytest
from astropy.time import Time
from spiceypy.utils.exceptions import SpiceSPKINSUFFDATA

from wis.kernels import DE430, GAIA, HST, JWST, KEPLER, TESS
from wis.wis import Wis

pytestmark = pytest.mark.integration


@pytest.fixture(autouse=True)
def clear_cache_between_tests() -> None:
    """Clear the cached Horizons queries after each test."""
    yield
    Wis.cache_get_obs_helio_equ_AU.clear()


# -------------------------------------------------------------------
# TESS (C57, JPL -95)
# -------------------------------------------------------------------


def test_TESS() -> None:
    """Test TESS (C57) heliocentric position at a single epoch.

    *** DATA FROM EXPLICIT HORIZONS QUERY ***
    *******************************************************************************
    Ephemeris / WWW_USER Tue Jan 26 06:45:47 2021 Pasadena, USA      / Horizons
    *******************************************************************************
    Target body name: TESS (spacecraft) (-95)         {source: TESS_merged}
    Center body name: Sun (10)                        {source: TESS_merged}
    Center-site name: BODY CENTER
    *******************************************************************************
    Start time      : A.D. 2018-Aug-07 07:53:59.2365 TDB
    Stop  time      : A.D. 2018-Aug-08 07:53:59.2365 TDB
    Step-size       : 1440 minutes
    *******************************************************************************
    Output units    : AU-D
    Reference frame : ICRF
    *******************************************************************************
    $$SOE
    2458337.829157830 = A.D. 2018-Aug-07 07:53:59.2365 TDB
    X = 7.101323039968829E-01 Y =-6.636211705364583E-01 Z =-2.882396266749596E-01
    $$EOE
    """
    times = Time([2458337.829157830], format="jd", scale="tdb")
    obscode = "C57"
    with Wis(kernels=[DE430, TESS]) as W:
        W.get_obs_helio_equ_AU(obscode, times)
        expectedPosns = np.array(
            [[7.101323039968829e-01, -6.636211705364583e-01, -2.882396266749596e-01]]
        )
        assert np.allclose(W.obs_helio_equ_AU, expectedPosns, rtol=1e-08, atol=1e-08), (
            f"TESS position not as expected:\n"
            f"  returned: {W.obs_helio_equ_AU}\n"
            f"  expected: {expectedPosns}"
        )


def test_TESS_multi_epoch() -> None:
    """Test TESS (C57) heliocentric position at two consecutive epochs.

    *** DATA FROM EXPLICIT HORIZONS QUERY ***
    (same query as test_TESS, two-day output)
    *******************************************************************************
    $$SOE
    2458337.829157830 = A.D. 2018-Aug-07 07:53:59.2365 TDB
    X = 7.101323039968829E-01 Y =-6.636211705364583E-01 Z =-2.882396266749596E-01
    2458338.829157830 = A.D. 2018-Aug-08 07:53:59.2365 TDB
    X = 7.228838752596055E-01 Y =-6.530547342937241E-01 Z =-2.830064804389050E-01
    $$EOE
    """
    times = Time([2458337.829157830, 2458338.829157830], format="jd", scale="tdb")
    obscode = "C57"
    with Wis(kernels=[DE430, TESS]) as W:
        W.get_obs_helio_equ_AU(obscode, times)
        expectedPosns = np.array(
            [
                [7.101323039968829e-01, -6.636211705364583e-01, -2.882396266749596e-01],
                [7.228838752596055e-01, -6.530547342937241e-01, -2.830064804389050e-01],
            ]
        )
        assert np.allclose(W.obs_helio_equ_AU, expectedPosns, rtol=1e-08, atol=1e-08), (
            f"TESS multi-epoch position not as expected:\n"
            f"  returned: {W.obs_helio_equ_AU}\n"
            f"  expected: {expectedPosns}"
        )


def test_TESS_before_launch() -> None:
    """Test that requesting TESS positions before its 2018 launch raises SpiceSPKINSUFFDATA."""
    times = Time([2455197.585104], format="jd", scale="tdb")  # A.D. 2010 January 1
    obscode = "C57"
    with Wis(kernels=[DE430, TESS]) as W, pytest.raises(SpiceSPKINSUFFDATA):
        W.get_obs_helio_equ_AU(obscode, times)


# -------------------------------------------------------------------
# Kepler / K2 (C55, JPL -227)
# -------------------------------------------------------------------


def test_Kepler() -> None:
    """Test Kepler/K2 (C55) heliocentric position at two epochs.

    *** DATA FROM EXPLICIT HORIZONS QUERY ***
    *******************************************************************************
    Target body name: Kepler (spacecraft) (-227)      {source: KEPLER_FINAL_56_traj}
    Center body name: Sun (10)                        {source: DE431mx}
    Center-site name: BODY CENTER
    *******************************************************************************
    Start time      : A.D. 2018-Aug-07 07:53:59.2365 TDB
    Stop  time      : A.D. 2018-Aug-08 07:53:59.2365 TDB
    Step-size       : 1440 minutes
    *******************************************************************************
    Output units    : AU-D
    Reference frame : ICRF
    *******************************************************************************
    $$SOE
    2458337.829157830 = A.D. 2018-Aug-07 07:53:59.2365 TDB
    X =-3.247439631457193E-01 Y =-9.176995632113913E-01 Z =-3.890277674336675E-01
    2458338.829157830 = A.D. 2018-Aug-08 07:53:59.2365 TDB
    X =-3.090609977353972E-01 Y =-9.224171671345395E-01 Z =-3.910919864336775E-01
    $$EOE
    """
    times = Time([2458337.829157830, 2458338.829157830], format="jd", scale="tdb")
    obscode = "C55"
    with Wis(kernels=[DE430, KEPLER]) as W:
        W.get_obs_helio_equ_AU(obscode, times)
        expectedPosns = np.array(
            [
                [
                    -3.247439631457193e-01,
                    -9.176995632113913e-01,
                    -3.890277674336675e-01,
                ],
                [
                    -3.090609977353972e-01,
                    -9.224171671345395e-01,
                    -3.910919864336775e-01,
                ],
            ]
        )
        assert np.allclose(W.obs_helio_equ_AU, expectedPosns, rtol=1e-08, atol=1e-08), (
            f"Kepler position not as expected:\n"
            f"  returned: {W.obs_helio_equ_AU}\n"
            f"  expected: {expectedPosns}"
        )


# -------------------------------------------------------------------
# HST (250, JPL -48)
# -------------------------------------------------------------------


def test_HST() -> None:
    """Test Hubble Space Telescope (250) heliocentric position at two epochs.

    HST is in low Earth orbit (~570 km altitude), so its heliocentric position
    is dominated by Earth's orbital position; the small LEO offset tests that
    the satellite kernel path is exercised correctly.

    *** DATA FROM EXPLICIT HORIZONS QUERY ***
    Horizons API query (2026-05-27):
      COMMAND='-48', CENTER=500@10, OUT_UNITS=AU-D,
      REF_PLANE=FRAME, REF_SYSTEM=ICRF, VEC_CORR=NONE
    *******************************************************************************
    Target body name: Hubble Space Telescope (spacecraft) (-48) {source: hst}
    Center body name: Sun (10)                        {source: DE441}
    Center-site name: BODY CENTER
    *******************************************************************************
    Start time      : A.D. 2018-Aug-07 00:00:00.0000 TDB
    Stop  time      : A.D. 2018-Aug-08 00:00:00.0000 TDB
    Step-size       : 1440 minutes
    *******************************************************************************
    Output units    : AU-D
    Reference frame : ICRF
    *******************************************************************************
    $$SOE
    2458337.500000000 = A.D. 2018-Aug-07 00:00:00.0000 TDB
    X = 7.072406603204043E-01 Y =-6.670186802941361E-01 Z =-2.891679366364408E-01
    VX= 1.180217262395590E-02 VY= 1.502865400889255E-02 VZ= 3.164781826684843E-03
    LT= 5.857871583901436E-03 RG= 1.014259023647485E+00 RR=-2.556122227269186E-03
    2458338.500000000 = A.D. 2018-Aug-08 00:00:00.0000 TDB
    X = 7.191882705213363E-01 Y =-6.559509062537210E-01 Z =-2.843896913347406E-01
    VX= 9.199438954794491E-03 VY= 1.461672978699064E-02 VZ= 4.624416899014773E-03
    LT= 5.856902014896860E-03 RG= 1.014091147978335E+00 RR=-4.227297577379665E-03
    $$EOE
    """
    times = Time([2458337.500000000, 2458338.500000000], format="jd", scale="tdb")
    obscode = "250"
    with Wis(kernels=[DE430, HST]) as W:
        W.get_obs_helio_equ_AU(obscode, times)
        expectedPosns = np.array(
            [
                [7.072406603204043e-01, -6.670186802941361e-01, -2.891679366364408e-01],
                [7.191882705213363e-01, -6.559509062537210e-01, -2.843896913347406e-01],
            ]
        )
        assert np.allclose(W.obs_helio_equ_AU, expectedPosns, rtol=1e-08, atol=1e-08), (
            f"HST position not as expected:\n"
            f"  returned: {W.obs_helio_equ_AU}\n"
            f"  expected: {expectedPosns}"
        )


# -------------------------------------------------------------------
# JWST (274, JPL -170)
# -------------------------------------------------------------------


def test_JWST() -> None:
    """Test James Webb Space Telescope (274) heliocentric position at two epochs.

    JWST orbits the Sun-Earth L2 point (~1.5 million km from Earth).
    These epochs are ~5 months after JWST's Dec 2021 launch, well within
    the reconstructed kernel coverage.

    *** DATA FROM EXPLICIT HORIZONS QUERY ***
    Horizons API query (2026-05-27):
      COMMAND='-170', CENTER=500@10, OUT_UNITS=AU-D,
      REF_PLANE=FRAME, REF_SYSTEM=ICRF, VEC_CORR=NONE
    *******************************************************************************
    Target body name: James Webb Space Telescope (spacecraft) (-170) {source: JWST_merged}
    Center body name: Sun (10)                        {source: DE441}
    Center-site name: BODY CENTER
    *******************************************************************************
    Start time      : A.D. 2022-May-01 00:00:00.0000 TDB
    Stop  time      : A.D. 2022-May-02 00:00:00.0000 TDB
    Step-size       : 1440 minutes
    *******************************************************************************
    Output units    : AU-D
    Reference frame : ICRF
    *******************************************************************************
    $$SOE
    2459700.500000000 = A.D. 2022-May-01 00:00:00.0000 TDB
    X =-7.719857845277884E-01 Y =-6.061748244652156E-01 Z =-2.612099115227776E-01
    VX= 1.103824233396557E-02 VY=-1.222455977427884E-02 VZ=-5.387169348362892E-03
    LT= 5.866177186852640E-03 RG= 1.015697094219609E+00 RR= 2.914611431622722E-04
    2459701.500000000 = A.D. 2022-May-02 00:00:00.0000 TDB
    X =-7.608369737493887E-01 Y =-6.183085948663846E-01 Z =-2.665588060953452E-01
    VX= 1.125877430663032E-02 VY=-1.204244507134428E-02 VZ=-5.310360520911305E-03
    LT= 5.867858455653154E-03 RG= 1.015988196888501E+00 RR= 2.907306212110479E-04
    $$EOE
    """
    times = Time([2459700.500000000, 2459701.500000000], format="jd", scale="tdb")
    obscode = "274"
    with Wis(kernels=[DE430, JWST]) as W:
        W.get_obs_helio_equ_AU(obscode, times)
        expectedPosns = np.array(
            [
                [
                    -7.719857845277884e-01,
                    -6.061748244652156e-01,
                    -2.612099115227776e-01,
                ],
                [
                    -7.608369737493887e-01,
                    -6.183085948663846e-01,
                    -2.665588060953452e-01,
                ],
            ]
        )
        assert np.allclose(W.obs_helio_equ_AU, expectedPosns, rtol=1e-08, atol=1e-08), (
            f"JWST position not as expected:\n"
            f"  returned: {W.obs_helio_equ_AU}\n"
            f"  expected: {expectedPosns}"
        )


# -------------------------------------------------------------------
# Gaia (258, ESA kernel body ID -123 / Horizons ID -139479)
# -------------------------------------------------------------------


def test_Gaia() -> None:
    """Test Gaia (258) heliocentric position at two epochs.

    wis.py uses the ESA-provided SPICE kernel, which stores Gaia under body
    ID -123 (ESA-internal convention). JPL Horizons uses -139479 (standard NAIF
    ID).

    *** DATA FROM EXPLICIT HORIZONS QUERY ***
    Horizons API query (2026-05-27):
      COMMAND='-139479', CENTER=500@10, OUT_UNITS=AU-D,
      REF_PLANE=FRAME, REF_SYSTEM=ICRF, VEC_CORR=NONE
    *******************************************************************************
    Target body name: Gaia (spacecraft) (-139479)     {source: gaia_merged}
    Center body name: Sun (10)                        {source: gaia_merged}
    Center-site name: BODY CENTER
    *******************************************************************************
    Start time      : A.D. 2014-Jan-20 00:00:00.0000 TDB
    Stop  time      : A.D. 2014-Jan-21 00:00:00.0000 TDB
    Step-size       : 1440 minutes
    *******************************************************************************
    Output units    : AU-D
    Reference frame : ICRF
    *******************************************************************************
    $$SOE
    2456677.500000000 = A.D. 2014-Jan-20 00:00:00.0000 TDB
    X =-4.896140352011714E-01 Y = 7.924816137052370E-01 Z = 3.428170211395259E-01
    VX=-1.537562780581752E-02 VY=-7.847388053142350E-03 VZ=-3.369248884536836E-03
    LT= 5.732831168896983E-03 RG= 9.926089469221041E-01 RR= 1.553245721144119E-04
    2456678.500000000 = A.D. 2014-Jan-21 00:00:00.0000 TDB
    X =-5.049128747257849E-01 Y = 7.845095846687323E-01 Z = 3.393943270525736E-01
    VX=-1.522127637485401E-02 VY=-8.096207231852280E-03 VZ=-3.475951754586475E-03
    LT= 5.733727986962654E-03 RG= 9.927642261566603E-01 RR= 1.552714409870152E-04
    $$EOE
    """
    times = Time([2456677.500000000, 2456678.500000000], format="jd", scale="tdb")
    obscode = "258"
    with Wis(kernels=[DE430, GAIA]) as W:
        W.get_obs_helio_equ_AU(obscode, times)
        expectedPosns = np.array(
            [
                [-4.896140352011714e-01, 7.924816137052370e-01, 3.428170211395259e-01],
                [-5.049128747257849e-01, 7.845095846687323e-01, 3.393943270525736e-01],
            ]
        )
        assert np.allclose(W.obs_helio_equ_AU, expectedPosns, rtol=1e-08, atol=1e-08), (
            f"Gaia position not as expected:\n"
            f"  returned: {W.obs_helio_equ_AU}\n"
            f"  expected: {expectedPosns}"
        )
