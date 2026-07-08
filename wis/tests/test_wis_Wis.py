"""Tests for the Wis class."""

import json
import os.path
from pathlib import Path
from typing import Never

import numpy as np
import pytest
import spiceypy as sp
from astropy.time import Time
from spiceypy.utils.exceptions import SpiceFRAMEDATANOTFOUND

from wis.constants import PhysicalConstants
from wis.kernels import DE430, DE440, TESS
from wis.obscodes import MPCObsCodes
from wis.wis import Wis

pytestmark = pytest.mark.integration

# -------------------------------------------------------------------
# Tests of basic functionalities
# -------------------------------------------------------------------


@pytest.fixture(autouse=True)
def clear_cache_between_tests() -> None:
    """Clear the Wis cache after each test."""
    yield  # test body will run here
    Wis.cache_get_obs_helio_equ_AU.clear()  # ensures that after each test, the cache is cleared


def test_Wis_instantiation_successful() -> None:
    """Test that a Wis object can be instantiated with explicit kernels."""
    # Instantiate a Wis object with DE430 kernel
    with Wis(kernels=DE430) as W:
        assert isinstance(W, Wis), f"Object is not an instance of Wis: {W}"
        # Check that we have access to the attributes from the parent MPCObsCodes class
        assert hasattr(
            W, "geocentric_xyz_dict"
        ), f"Object does not have geocentric_xyz_dict attribute: {W}"
        assert (
            W.geocentric_xyz_dict
        ), f"Geocentric XYZ dict is empty: {W.geocentric_xyz_dict}"
        assert hasattr(
            W, "two_line_dict"
        ), f"Object does not have two_line_dict attribute: {W}"
        assert W.two_line_dict, f"Two-line dict is empty: {W.two_line_dict}"

        # Check that the class variables are set as expected
        assert W.center == "SUN", f"Center not as expected: {W.center}"
        assert W.frame == "J2000", f"Frame not as expected: {W.frame}"
        assert W.abcorr == "NONE", f"Abcorr not as expected: {W.abcorr}"

        # Check that spice kernels have been loaded
        assert sp.ktotal("ALL") > 0, f"No kernels loaded: {sp.ktotal('ALL')}"
        assert sp.ktotal("SPK") > 0, f"No SPK kernels loaded: {sp.ktotal('SPK')}"

    # Check that spice kernels have been cleared outside of the context manager
    assert sp.ktotal("ALL") == 0, f"kernels still loaded: {sp.ktotal('ALL')}"
    assert sp.ktotal("SPK") == 0, f"SPK still kernels loaded: {sp.ktotal('SPK')}"


def test_Wis_instantiation_no_kernels_raises() -> None:
    """Test that Wis instantiation raises ValueError when no kernels specified."""
    with pytest.raises(ValueError, match="Must specify kernels"):
        Wis(kernels=None)


def test_Wis_instantiation_empty_list_raises() -> None:
    """Test that Wis instantiation raises ValueError with empty kernel list."""
    with pytest.raises(ValueError, match="kernels list cannot be empty"), Wis(
        kernels=[]
    ):
        pass


def test_Wis_instantiation_with_list() -> None:
    """Test that Wis can be instantiated with a list of kernels."""
    with Wis(kernels=[DE430, TESS]) as W:
        assert isinstance(W, Wis)
        # Check that both kernels were loaded
        assert len(W.loaded_kernels) == 2
        kernel_names = [k.name for k in W.loaded_kernels]
        assert "DE430" in kernel_names
        assert "TESS" in kernel_names


def test_Wis_instantiation_with_DE440() -> None:
    """Test that Wis can be instantiated with DE440 kernel."""
    with Wis(kernels=DE440) as W:
        assert isinstance(W, Wis)
        assert len(W.loaded_kernels) == 1
        assert W.loaded_kernels[0].name == "DE440"


def test__check_input_formats() -> None:
    """Test that instantiation fails if obscode is not a string."""
    with pytest.raises(ValueError), Wis(kernels=DE430) as W:
        W._check_input_formats(
            95,
            Time([2458337.829157830, 2458338.829157830], format="jd", scale="tdb"),
        )
    with pytest.raises(ValueError), Wis(kernels=DE430) as W:
        W._check_input_formats(
            None,
            Time([2458337.829157830, 2458338.829157830], format="jd", scale="tdb"),
        )
    with pytest.raises(ValueError), Wis(kernels=DE430) as W:
        W._check_input_formats(
            [95],
            Time([2458337.829157830, 2458338.829157830], format="jd", scale="tdb"),
        )
    with pytest.raises(ValueError), Wis(kernels=DE430) as W:
        W._check_input_formats("-95", [2458337.829157830, 2458338.829157830])
    with pytest.raises(ValueError), Wis(kernels=DE430) as W:
        W._check_input_formats("-95", None)


def test__convert_posn() -> None:
    """Test that the _convert_posn method works as expected."""
    with Wis(kernels=DE430) as W:
        posns = np.array([1, 2, 3])  # <- Inputs in km (as per SPICE)
        # Call the method to convert the position
        converted_posns = W._convert_posn(posns)
        # Assert that the returned position has the expected shape & values
        assert converted_posns.shape == (
            3,
        ), f"Converted posn not as expected: {converted_posns}"
        assert np.allclose(
            converted_posns,
            np.atleast_1d(posns) / PhysicalConstants.au_km,
            rtol=1e-09,
            atol=1e-09,
        ), f"Converted posn not as expected: {converted_posns}"


def test__convert_vel() -> None:
    """Test that the _convert_vel method works as expected."""
    with Wis(kernels=DE430) as W:
        vels = np.array([1, 2, 3])  # <- Inputs are in km/s (as per SPICE)

        # Call the method to convert the velocity
        converted_vels = W._convert_vel(vels)

        # Assert that the returned velocity has the expected shape & values
        assert converted_vels.shape == (
            3,
        ), f"Converted vels not as expected: {converted_vels}"
        conversion_factor = 149597870.700 / (3600 * 24)  # 1 AU/day = 1731.45683681 km/s
        expected_vels = np.atleast_1d(vels) / conversion_factor
        assert np.allclose(
            converted_vels, expected_vels, rtol=1e-09, atol=1e-09
        ), f"Converted vels not as expected: {converted_vels}"


def test_wis_Station__convert_ltts() -> None:
    """Test that the _convert_ltts method works as expected."""
    with Wis(kernels=DE430) as W:
        ltts = np.array([1, 2, 3])
        # Call the method to convert the position
        converted_ltts = W._convert_ltts(ltts)
        # Assert that the returned position has the expected shape & values
        assert converted_ltts.shape == (
            3,
        ), f"Converted ltts not as expected: {converted_ltts}"
        assert np.allclose(
            converted_ltts,
            np.atleast_1d(ltts) / PhysicalConstants.day_s,
            rtol=1e-09,
            atol=1e-09,
        ), f"Converted posn not as expected: {converted_ltts}"


# -------------------------------------------------------------------
# Check the behaviour of Wis when it cannot connect to the database
# -------------------------------------------------------------------


def test_Wis_no_db_connection(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Test backup mechanism when MPC ObsCodes API is unavailable.

    This test verifies that:
    1. A Wis instance with API access successfully writes a backup obscode.json file
    2. The backup file contains exact copies of the data returned by the API
    3. A Wis instance without API access can use the backup file (fallback=True)
    4. A Wis instance without API access raises ConnectionError when fallback=False

    The test uses mock API responses based on test_data/obscode.json to ensure
    deterministic behavior independent of actual API data changes.
    """
    # Load test data to use as mock API response
    test_data_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "test_data",
        "obscode.json",
    )
    with open(test_data_path) as f:
        d = json.load(f)
    expected_ground = d["GeocentricXYZ_as_lists"]
    expected_twoline = d["TwoLine"]
    # Convert to numpy arrays as expected by query_obscodes_api
    mock_geocentric = {k: np.array(v) for k, v in expected_ground.items()}
    mock_twoline = expected_twoline

    # Use a temporary local obscode file to avoid cached data
    temp_file = tmp_path / "obscode.json"
    monkeypatch.setattr(Wis, "local_obscode_file", temp_file)
    monkeypatch.setattr(MPCObsCodes, "local_obscode_file", temp_file)

    def mock_query_obscodes_api_success(
        self: MPCObsCodes,
    ) -> tuple[dict[str, np.ndarray], dict[str, bool]]:
        return mock_geocentric, mock_twoline

    monkeypatch.setattr(Wis, "query_obscodes_api", mock_query_obscodes_api_success)
    monkeypatch.setattr(
        MPCObsCodes, "query_obscodes_api", mock_query_obscodes_api_success
    )

    # Create a standard Wis instance WITH connection
    with Wis(kernels=DE430) as W:
        pass

    # Check that the backup obscode.json has been saved as expected
    # (TODO: Move to test_obscodes.py)
    assert os.path.isfile(W.local_obscode_file)
    with open(W.local_obscode_file) as f:
        d = json.load(f)
        backup_ground, backup_twoline = d["GeocentricXYZ_as_lists"], d["TwoLine"]

    for k, v in expected_ground.items():
        assert k in backup_ground, "Backup dict not as expected"
        # Backup should contain exact copies of the data returned by the API
        # Use array_equal for exact comparison, as backup should be identical to API response
        assert np.array_equal(
            np.array(v), np.array(backup_ground[k])
        ), f"Backup dict-array not as expected for key {k}: {v} vs {backup_ground[k]}"
    for k, v in expected_twoline.items():
        assert k in backup_twoline, "Backup dict not as expected"
        # Two-line codes should be exact boolean matches
        assert v == backup_twoline[k], f"Backup dict not as expected for key {k}"

    # Now create a Wis instance WITHOUT a connection to the database
    # (have to monkeypatch the query_obscodes_api method to raise an exception)
    def mock_query_obscodes_api(self: MPCObsCodes) -> Never:
        raise Exception("Test exception")

    monkeypatch.setattr(Wis, "query_obscodes_api", mock_query_obscodes_api)
    monkeypatch.setattr(MPCObsCodes, "query_obscodes_api", mock_query_obscodes_api)

    with Wis(kernels=DE430) as W_noconn:
        # Check that W_noconn has access to the backup obscode.json
        assert os.path.isfile(W_noconn.local_obscode_file)
        geocentric_xyz_dict, _two_line_dict = W_noconn.get_geocentric_xyz_dict(
            fallback=True
        )
        for k, v in expected_ground.items():
            assert k in geocentric_xyz_dict, "W_noconn dict not as expected"
            # When fallback=True and API fails, should load numpy arrays from backup
            # These should be exact matches to the original API data
            assert np.array_equal(
                np.array(v), geocentric_xyz_dict[k]
            ), f"W_noconn dict-array not as expected for key {k}"

    # Check that a Wis instance WITHOUT a connection to the database CANNOT
    # access the required data if fallback is set False
    with Wis(kernels=DE430) as W_noconn_nofallback:
        W_noconn_nofallback = Wis.__new__(Wis)
        assert os.path.isfile(W_noconn_nofallback.local_obscode_file)
        with pytest.raises(ConnectionError):
            geocentric_xyz_dict, _two_line_dict = (
                W_noconn_nofallback.get_geocentric_xyz_dict(fallback=False)
            )


# -------------------------------------------------------------------
# Tests of accuracy for ground-based observatories
# -------------------------------------------------------------------


def test_Ground_geocentric() -> None:
    """Test observatory position calculation against Horizons (km).

    The Horizons query below is returning the position of the observatory w.r.t. the center of the Earth
    I.e. this is a GEOCENTRIC position, not a heliocentric one
    This means that we have to compare the numbers to the `obs_geo_equ` quantity.
    """
    # *** DATA FROM EXPLICIT HORIZONS QUERY -------------
    """
*******************************************************************************
Ephemeris / WWW_USER Tue Jan 26 11:12:25 2021 Pasadena, USA      / Horizons
*******************************************************************************
Target body name: Earth (399)                     {source: DE431mx}
Center body name: Earth (399)                     {source: DE431mx}
Center-site name: Pan-STARRS 1, Haleakala
*******************************************************************************
Start time      : A.D. 2000-Jan-01 12:01:04.1839 TDB
Stop  time      : A.D. 2000-Jan-02 12:01:04.1839 TDB
Step-size       : 0 steps
*******************************************************************************
Center geodetic : 203.744100,20.7071888,3.0763821 {E-lon(deg),Lat(deg),Alt(km)}
Center cylindric: 203.744100,5971.48324,2242.1878 {E-lon(deg),Dxy(km),Dz(km)}
Center pole/equ : High-precision EOP model        {East-longitude positive}
Center radii    : 6378.1 x 6378.1 x 6356.8 km     {Equator, meridian, pole}
Output units    : KM-S
Output type     : GEOMETRIC cartesian states
Output format   : 3 (position, velocity, LT, range, range-rate)
EOP file        : eop.210125.p210418
EOP coverage    : DATA-BASED 1962-JAN-20 TO 2021-JAN-25. PREDICTS-> 2021-APR-17
Reference frame : ICRF
*******************************************************************************
JDTDB
   X     Y     Z
   VX    VY    VZ
   LT    RG    RR
*******************************************************************************
$$SOE
2451545.000742869 = A.D. 2000-Jan-01 12:01:04.1839 TDB [del_T=     64.183904 s]
 X = 3.357062612610595E+03 Y =-4.938472797753120E+03 Z =-2.242238952821062E+03
 VX= 3.601236917337654E-01 VY= 2.447964660859150E-01 VZ= 1.654269866964587E-05
 LT= 2.127658354697273E-02 RG= 6.378559279389312E+03 RR=-4.126854789751626E-17
2451546.000742869 = A.D. 2000-Jan-02 12:01:04.1839 TDB [del_T=     64.183933 s]
 X = 3.441514318240966E+03 Y =-4.879997205156549E+03 Z =-2.242236596724388E+03
 VX= 3.558595984886408E-01 VY= 2.509548321430072E-01 VZ= 1.651208609599962E-05
 LT= 2.127658354697273E-02 RG= 6.378559279389311E+03 RR= 8.360100975126858E-18
$$EOE
*******************************************************************************
Coordinate system description:

  International Celestial Reference Frame (ICRF)

    The ICRF is an adopted reference frame whose axes are defined relative to
    fixed extragalactic radio sources distributed across the sky.

    The ICRF was aligned with the prior FK5/J2000 dynamical system at the ~0.02
    arcsecond level but is not identical and has no associated standard epoch.

  Symbol meaning:

    JDTDB    Julian Day Number, Barycentric Dynamical Time
    del_T    Time-scale conversion difference TDB - UT (s)
      X      X-component of position vector (km)
      Y      Y-component of position vector (km)
      Z      Z-component of position vector (km)
      VX     X-component of velocity vector (km/sec)
      VY     Y-component of velocity vector (km/sec)
      VZ     Z-component of velocity vector (km/sec)
      LT     One-way down-leg Newtonian light-time (sec)
      RG     Range; distance from coordinate center (km)
      RR     Range-rate; radial velocity wrt coord. center (km/sec)

Geometric states/elements have no aberrations applied.


 Computations by ...
     Solar System Dynamics Group, Horizons On-Line Ephemeris System
     4800 Oak Grove Drive, Jet Propulsion Laboratory
     Pasadena, CA  91109   USA
     Information  : https://ssd.jpl.nasa.gov/
     Documentation: https://ssd.jpl.nasa.gov/?horizons_doc
     Connect      : https://ssd.jpl.nasa.gov/?horizons (browser)
                    telnet ssd.jpl.nasa.gov 6775       (command-line)
                    e-mail command interface available
                    Script and CGI interfaces available
     Author       : Jon.D.Giorgini@jpl.nasa.gov
*******************************************************************************
    """
    # Time & Obscode of interest
    times = Time([2451545.000742869, 2451546.000742869], format="jd", scale="tdb")
    obscode = "F51"

    # Instantiate & call the get_obs_helio_equ_AU method
    with Wis(kernels=DE430) as W:
        W.get_obs_helio_equ_AU(obscode, times)

        # Assert that the calculated quantities have the expected numerical values
        # NB The above query is from F51 to Sun, rather than Sun to F51 (limitations of Horizons query)
        # - Hence MINUS SIGN IN FRONT OF EXPECTED POSITIONS ARRAY
        # X = 3.357062612610595E+03 Y =-4.938472797753120E+03 Z =-2.242238952821062E+03
        # X = 3.441514318240966E+03 Y =-4.879997205156549E+03 Z =-2.242236596724388E+03
        expectedPosns = -1.0 * np.array(
            [
                [3.357062612610595e03, -4.938472797753120e03, -2.242238952821062e03],
                [3.441514318240966e03, -4.879997205156549e03, -2.242236596724388e03],
            ]
        )
        assert np.allclose(
            W.obs_geo_equ, expectedPosns, rtol=1e-06, atol=1e-01
        ), f" Not close enough to expected values: returned=[{W.obs_geo_equ!r}], expected=[{expectedPosns!r}]"


def test_Ground_B() -> None:
    """Test geocenter position calculation against Horizons (AU)."""
    # *** DATA FROM EXPLICIT HORIZONS QUERY -------------
    """
*******************************************************************************
Ephemeris / WWW_USER Tue Jan 26 11:23:52 2021 Pasadena, USA      / Horizons
*******************************************************************************
Target body name: Earth (399)                     {source: DE431mx}
Center body name: Earth (399)                     {source: DE431mx}
Center-site name: Pan-STARRS 1, Haleakala
*******************************************************************************
Start time      : A.D. 2000-Jan-01 12:01:04.1839 TDB
Stop  time      : A.D. 2000-Jan-02 12:01:04.1839 TDB
Step-size       : 0 steps
*******************************************************************************
Center geodetic : 203.744100,20.7071888,3.0763821 {E-lon(deg),Lat(deg),Alt(km)}
Center cylindric: 203.744100,5971.48324,2242.1878 {E-lon(deg),Dxy(km),Dz(km)}
Center pole/equ : High-precision EOP model        {East-longitude positive}
Center radii    : 6378.1 x 6378.1 x 6356.8 km     {Equator, meridian, pole}
Output units    : AU-D
Output type     : GEOMETRIC cartesian states
Output format   : 3 (position, velocity, LT, range, range-rate)
EOP file        : eop.210125.p210418
EOP coverage    : DATA-BASED 1962-JAN-20 TO 2021-JAN-25. PREDICTS-> 2021-APR-17
Reference frame : ICRF
*******************************************************************************
JDTDB
   X     Y     Z
   VX    VY    VZ
   LT    RG    RR
*******************************************************************************
$$SOE
2451545.000742869 = A.D. 2000-Jan-01 12:01:04.1839 TDB [del_T=     64.183904 s]
 X = 2.244057750890565E-05 Y =-3.301165166753353E-05 Z =-1.498844162907635E-05
 VX= 2.079888358049827E-04 VY= 1.413817895325368E-04 VZ= 9.554207946740535E-09
 LT= 2.462567540158880E-07 RG= 4.263803521763170E-05 RR=-1.238731504259479E-20
2451546.000742869 = A.D. 2000-Jan-02 12:01:04.1839 TDB [del_T=     64.183933 s]
 X = 2.300510229281603E-05 Y =-3.262076647429548E-05 Z =-1.498842587954287E-05
 VX= 2.055261158835369E-04 VY= 1.449385435481056E-04 VZ= 9.536527706034836E-09
 LT= 2.462567540158880E-07 RG= 4.263803521763169E-05 RR=-8.937480661616926E-21
$$EOE
*******************************************************************************
Coordinate system description:

  International Celestial Reference Frame (ICRF)

    The ICRF is an adopted reference frame whose axes are defined relative to
    fixed extragalactic radio sources distributed across the sky.

    The ICRF was aligned with the prior FK5/J2000 dynamical system at the ~0.02
    arcsecond level but is not identical and has no associated standard epoch.

  Symbol meaning [1 au= 149597870.700 km, 1 day= 86400.0 s]:

    JDTDB    Julian Day Number, Barycentric Dynamical Time
    del_T    Time-scale conversion difference TDB - UT (s)
      X      X-component of position vector (au)
      Y      Y-component of position vector (au)
      Z      Z-component of position vector (au)
      VX     X-component of velocity vector (au/day)
      VY     Y-component of velocity vector (au/day)
      VZ     Z-component of velocity vector (au/day)
      LT     One-way down-leg Newtonian light-time (day)
      RG     Range; distance from coordinate center (au)
      RR     Range-rate; radial velocity wrt coord. center (au/day)

Geometric states/elements have no aberrations applied.


 Computations by ...
     Solar System Dynamics Group, Horizons On-Line Ephemeris System
     4800 Oak Grove Drive, Jet Propulsion Laboratory
     Pasadena, CA  91109   USA
     Information  : https://ssd.jpl.nasa.gov/
     Documentation: https://ssd.jpl.nasa.gov/?horizons_doc
     Connect      : https://ssd.jpl.nasa.gov/?horizons (browser)
                    telnet ssd.jpl.nasa.gov 6775       (command-line)
                    e-mail command interface available
                    Script and CGI interfaces available
     Author       : Jon.D.Giorgini@jpl.nasa.gov
*******************************************************************************
    """
    # Time & Obscode of interest
    times = Time([2451545.000742869, 2451546.000742869], format="jd", scale="tdb")
    obscode = "F51"

    # Instantiate & call the get_obs_helio_equ_AU method
    with Wis(kernels=DE430) as W:
        # Call the method to get the observatory position
        W.get_obs_helio_equ_AU(obscode, times)
        # Assert that the calculated quantities have the expected numerical values
        # X = 2.244057750890565E-05 Y =-3.301165166753353E-05 Z =-1.498844162907635E-05
        # X = 2.300510229281603E-05 Y =-3.262076647429548E-05 Z =-1.498842587954287E-05
        expectedPosns = -1.0 * np.array(
            [
                [2.244057750890565e-05, -3.301165166753353e-05, -1.498844162907635e-05],
                [2.300510229281603e-05, -3.262076647429548e-05, -1.498842587954287e-05],
            ]
        )

        assert np.allclose(
            W.obs_geo_equ_AU, expectedPosns, rtol=1e-06, atol=1e-10
        ), f" Not close enough to expected values: returned=[{W.obs_geo_equ_AU!r}], expected=[{expectedPosns!r}]"


def test_Ground_C() -> None:
    """Test the overall heliocentric position of the observatory."""
    # *** DATA FROM EXPLICIT HORIZONS QUERY -------------
    """
*******************************************************************************
Ephemeris / WWW_USER Tue Jan 26 11:29:34 2021 Pasadena, USA      / Horizons
*******************************************************************************
Target body name: Sun (10)                        {source: DE431mx}
Center body name: Earth (399)                     {source: DE431mx}
Center-site name: Pan-STARRS 1, Haleakala
*******************************************************************************
Start time      : A.D. 2000-Jan-01 12:01:04.1839 TDB
Stop  time      : A.D. 2000-Jan-02 12:01:04.1839 TDB
Step-size       : 0 steps
*******************************************************************************
Center geodetic : 203.744100,20.7071888,3.0763821 {E-lon(deg),Lat(deg),Alt(km)}
Center cylindric: 203.744100,5971.48324,2242.1878 {E-lon(deg),Dxy(km),Dz(km)}
Center pole/equ : High-precision EOP model        {East-longitude positive}
Center radii    : 6378.1 x 6378.1 x 6356.8 km     {Equator, meridian, pole}
Output units    : AU-D
Output type     : GEOMETRIC cartesian states
Output format   : 3 (position, velocity, LT, range, range-rate)
EOP file        : eop.210125.p210418
EOP coverage    : DATA-BASED 1962-JAN-20 TO 2021-JAN-25. PREDICTS-> 2021-APR-17
Reference frame : ICRF
*******************************************************************************
JDTDB
   X     Y     Z
   VX    VY    VZ
   LT    RG    RR
*******************************************************************************
$$SOE
2451545.000742869 = A.D. 2000-Jan-01 12:01:04.1839 TDB [del_T=     64.183904 s]
 X = 1.771703233769980E-01 Y =-8.874593810516950E-01 Z =-3.847569536828423E-01
 VX= 1.741557375812744E-02 VY= 3.039755432093662E-03 VZ= 1.256493770641990E-03
 LT= 5.679456288207732E-03 RG= 9.833673728111324E-01 RR=-9.719801362883684E-05
2451546.000742869 = A.D. 2000-Jan-02 12:01:04.1839 TDB [del_T=     64.183933 s]
 X = 1.943505199554981E-01 Y =-8.844221447467095E-01 Z =-3.834405079856051E-01
 VX= 1.735627288621994E-02 VY= 3.320127567567683E-03 VZ= 1.376362758488653E-03
 LT= 5.679426593146453E-03 RG= 9.833622312706550E-01 RR=-9.248567476947815E-05
$$EOE
*******************************************************************************
Coordinate system description:

  International Celestial Reference Frame (ICRF)

    The ICRF is an adopted reference frame whose axes are defined relative to
    fixed extragalactic radio sources distributed across the sky.

    The ICRF was aligned with the prior FK5/J2000 dynamical system at the ~0.02
    arcsecond level but is not identical and has no associated standard epoch.

  Symbol meaning [1 au= 149597870.700 km, 1 day= 86400.0 s]:

    JDTDB    Julian Day Number, Barycentric Dynamical Time
    del_T    Time-scale conversion difference TDB - UT (s)
      X      X-component of position vector (au)
      Y      Y-component of position vector (au)
      Z      Z-component of position vector (au)
      VX     X-component of velocity vector (au/day)
      VY     Y-component of velocity vector (au/day)
      VZ     Z-component of velocity vector (au/day)
      LT     One-way down-leg Newtonian light-time (day)
      RG     Range; distance from coordinate center (au)
      RR     Range-rate; radial velocity wrt coord. center (au/day)

Geometric states/elements have no aberrations applied.


 Computations by ...
     Solar System Dynamics Group, Horizons On-Line Ephemeris System
     4800 Oak Grove Drive, Jet Propulsion Laboratory
     Pasadena, CA  91109   USA
     Information  : https://ssd.jpl.nasa.gov/
     Documentation: https://ssd.jpl.nasa.gov/?horizons_doc
     Connect      : https://ssd.jpl.nasa.gov/?horizons (browser)
                    telnet ssd.jpl.nasa.gov 6775       (command-line)
                    e-mail command interface available
                    Script and CGI interfaces available
     Author       : Jon.D.Giorgini@jpl.nasa.gov
*******************************************************************************
    """
    # Time & Obscode of interest
    times = Time([2451545.000742869, 2451546.000742869], format="jd", scale="tdb")
    obscode = "F51"

    # Instantiate & call the get_obs_helio_equ_AU method
    with Wis(kernels=DE430) as W:
        W.get_obs_helio_equ_AU(obscode, times)

        # Assert that the returned quantities have the expected numerical values
        # NB The above query is from F51 to Sun, rather than Sun to F51 (limitations of Horizons query)
        # - Hence MINUS SIGN IN FRONT OF EXPECTED POSITIONS ARRAY
        # X = 1.771703233769980E-01 Y =-8.874593810516950E-01 Z =-3.847569536828423E-01
        # X = 1.943505199554981E-01 Y =-8.844221447467095E-01 Z =-3.834405079856051E-01
        expectedPosns = -1.0 * np.array(
            [
                [1.771703233769980e-01, -8.874593810516950e-01, -3.847569536828423e-01],
                [1.943505199554981e-01, -8.844221447467095e-01, -3.834405079856051e-01],
            ]
        )
        assert np.allclose(
            W.obs_helio_equ_AU, expectedPosns, rtol=1e-06, atol=1e-06
        ), f" Not close enough to expected values: returned=[{W.obs_helio_equ_AU!r}], expected=[{expectedPosns!r}]"


def test_Ground_bary() -> None:
    """Test the barycentric equatorial position of F51 against Horizons (AU, ICRF).

    Horizons query: target=SSB(0), center=F51@399, DE441, REF_PLANE=FRAME (ICRF),
    REF_SYSTEM=ICRF, OUT_UNITS=AU-D, EPHEM_TYPE=VECTORS, VEC_TABLE=3.
    Result negated because Horizons returns SSB-relative-to-F51; we want F51-relative-to-SSB.

    DE441 is the same fit as DE440 extended over a longer time span; agreement at J2000
    should be at the sub-10-m level (~1e-10 AU per component).

    Horizons URL (queried 2026-05-27):
      https://ssd.jpl.nasa.gov/api/horizons.api?format=text
        &COMMAND=0&OBJ_DATA=NO&MAKE_EPHEM=YES&EPHEM_TYPE=VECTORS
        &CENTER=F51%40399&TLIST=2451545.000742869%202451546.000742869
        &TLIST_TYPE=JD&VEC_TABLE=3&OUT_UNITS=AU-D&CSV_FORMAT=NO
        &REF_SYSTEM=ICRF&REF_PLANE=FRAME

    Horizons output (SSB relative to F51):
    2451545.000742869 = A.D. 2000-Jan-01 12:01:04.1839 TDB
     X = 1.843074980163820E-01 Y =-8.848120375397996E-01 Z =-3.838340431535776E-01
    2451546.000742869 = A.D. 2000-Jan-02 12:01:04.1839 TDB
     X = 2.014823119363636E-01 Y =-8.817680468172032E-01 Z =-3.825145661113032E-01
    """
    times = Time([2451545.000742869, 2451546.000742869], format="jd", scale="tdb")
    obscode = "F51"

    with Wis(kernels=DE440) as W:
        result = W.get_obs_bary_equ_AU(obscode, times)
        assert result is not None
        posns = result

        # Horizons gives SSB relative to F51; negate for F51 relative to SSB
        expectedPosns = -1.0 * np.array(
            [
                [1.843074980163820e-01, -8.848120375397996e-01, -3.838340431535776e-01],
                [2.014823119363636e-01, -8.817680468172032e-01, -3.825145661113032e-01],
            ]
        )
        diff_km = (posns - expectedPosns) * 149597870.700
        # atol=1e-10 AU ~ 15 m; observed DE440 vs DE441 residuals are ~8 m
        assert np.allclose(posns, expectedPosns, rtol=0, atol=1e-10), (
            "Barycentric position not close enough to Horizons DE441.\n"
            f"Diff (km): {diff_km}"
        )


def test_Ground_D() -> None:
    """Test that an error is raised if we request an ephemeris for dates outside the kernel range."""
    # Make a Ground-object
    times = Time(
        [1455197.585104], format="jd", scale="tdb"
    )  # 1455197.585104 == 714 B.C. February 18
    obscode = "F51"
    # Instantiate & call the get_obs_helio_equ_AU method
    with Wis(kernels=DE430) as W, pytest.raises(SpiceFRAMEDATANOTFOUND):
        W.get_obs_helio_equ_AU(obscode, times)


# -------------------------------------------------------------------
# Tests of accuracy for excluded/unknown observatories
# -------------------------------------------------------------------


def test_wis_Geocenter_Unknown() -> None:
    """Test that unknown obscodes can be forced to be evaluated the same as the geocenter."""
    # Make a Satellite-object
    times = Time([2458337.829157830, 2458338.829157830], format="jd", scale="tdb")
    obscode = "500"

    # Instantiate & call the get_obs_helio_equ_AU method
    with Wis(kernels=DE430) as W_500:
        W_500.get_obs_helio_equ_AU(obscode, times)

    with Wis(kernels=DE430) as W_UNK:
        W_UNK.get_obs_helio_equ_AU("???", times, fallback_to_geo=True)

    # Check that the two objects have the same position
    # => The unknown obscode should be the same as 500 (the geocenter)
    assert np.allclose(
        W_UNK.obs_helio_equ_AU, W_500.obs_helio_equ_AU, rtol=1e-08, atol=1e-08
    ), "Unknown obscode should be the same as 500"


def test_excluded_via_wis() -> None:
    """Test that the 247 obs-code is excluded."""
    # Time & Obscode of interest
    time = Time([2458337.829157830, 2458338.829157830], format="jd", scale="tdb")
    obscode = "247"

    # Because we input obscode 247, we expect to get back a NoneType object
    with Wis(kernels=DE430) as W:
        assert isinstance(
            W.get_obs_helio_equ_AU(obscode, time, fallback_to_geo=False), type(None)
        )
