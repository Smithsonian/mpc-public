"""Tests for the Orbits API."""

import pytest
import responses

from mpc_api import MPCClient, MPCValidationError


ORBITS_URL = "https://data.minorplanetcenter.net/api/get-orb"


@pytest.fixture
def require_api(check_api):
    """Allow tests to skip if the Orbits API is unreachable."""
    check_api(ORBITS_URL)


SAMPLE_MPC_ORB = {
    "COM": {
        "coefficient_names": ["q", "e", "i", "node", "argperi", "tp"],
        "coefficient_values": [2.556, 0.0785, 10.59, 80.3, 73.6, 2459600.5],
        "coefficient_uncertainties": [0.001, 0.0001, 0.01, 0.01, 0.01, 0.1],
    },
    "CAR": {
        "coefficient_names": ["x", "y", "z", "vx", "vy", "vz"],
        "coefficient_values": [1.0, 2.0, 0.5, -0.01, 0.02, 0.001],
    },
    "designation_data": {
        "permid": "1",
        "packed_primary_provisional_designation": "I01A00A",
        "unpacked_primary_provisional_designation": "A801 AA",
    },
    "magnitude_data": {"H": 3.34, "G": 0.12},
}



# --- REAL TESTS THAT REALLY HIT THE API --------------
# -----------------------------------------------------

def test_get_orbit_real(require_api, client):
    """Hit the real API for Ceres orbit and verify structure."""
    result = client.get_orbit("Ceres")
    assert result is not None
    assert "COM" in result
    assert "CAR" in result
    assert "designation_data" in result
    assert result["designation_data"]["permid"] == "1"


def test_get_orbit_raw_real(require_api, client):
    """Hit the real API and verify raw orbit response structure."""
    result = client.get_orbit_raw("Ceres")
    assert isinstance(result, list)
    assert len(result) > 0
    assert "mpc_orb" in result[0]
    assert len(result[0]["mpc_orb"]) > 0



# --- MOCKED TESTS THAT FAKE THE RETURNED API RESPONSE ---
#     In the tests below, we mock the expected API response, and then verify that
#     the MPCClient correctly handles/passes-through that response.
#
#     `@responses.activate` - intercepts all requests HTTP calls in this test
#      `responses.get(URL, json=[...])` -- registers a fake GET response
#
#     This allows us to test the client's handling of the API responses, without
#     relying on the actual API, which may be unavailable during testing.
# ---------------------------------------------------------

@responses.activate
def test_get_orbit(client):
    responses.get(
        ORBITS_URL,
        json=[{"mpc_orb": [SAMPLE_MPC_ORB]}],
    )

    result = client.get_orbit("Ceres")
    assert result is not None
    assert "COM" in result
    assert "CAR" in result
    assert result["designation_data"]["permid"] == "1"


@responses.activate
def test_get_orbit_not_found(client):
    responses.get(
        ORBITS_URL,
        json=[{"mpc_orb": []}],
    )

    result = client.get_orbit("NotAnAsteroidName")
    assert result is None


@responses.activate
def test_get_orbit_raw(client):
    raw_response = [{"mpc_orb": [SAMPLE_MPC_ORB]}]
    responses.get(ORBITS_URL, json=raw_response)

    result = client.get_orbit_raw("Ceres")
    assert isinstance(result, list)
    assert "mpc_orb" in result[0]



# --- PURE TESTS OF INPUT VALIDATION LOGIC (NO API CALLS) ------
#     These tests verify that the client raises appropriate
#     exceptions when given invalid input parameters.
# ---------------------------------------------------------------

def test_get_orbit_empty_raises(client):
    with pytest.raises(MPCValidationError):
        client.get_orbit("")


def test_get_orbit_raw_empty_raises(client):
    with pytest.raises(MPCValidationError):
        client.get_orbit_raw("")
