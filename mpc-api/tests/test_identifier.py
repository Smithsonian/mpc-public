"""Tests for the Designation Identifier API."""

import pytest
import responses

from mpc_api import MPCClient, MPCValidationError


IDENTIFIER_URL = "https://data.minorplanetcenter.net/api/query-identifier"


@pytest.fixture
def require_api(check_api):
    """Allow tests to skip if the Identifier API is unreachable."""
    check_api(IDENTIFIER_URL)


# --- REAL TESTS THAT REALLY HIT THE API --------------
# -----------------------------------------------------

def test_identify_single_real(require_api, client):
    """Hit the real API with 'Ceres' and verify the response structure."""
    result = client.identify("Ceres")
    assert "Ceres" in result
    assert result["Ceres"]["found"] == 1
    assert result["Ceres"]["permid"] == "1"


def test_identify_multiple_real(require_api, client):
    """Hit the real API with multiple well-known objects."""
    result = client.identify(["Ceres", "Vesta"])
    assert "Ceres" in result
    assert "Vesta" in result
    assert result["Ceres"]["found"] == 1
    assert result["Vesta"]["found"] == 1



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
def test_identify_single(client):
    responses.get(
        IDENTIFIER_URL,
        json={
            "Sedna": {
                "found": 1,
                "permid": "90377",
                "name": "Sedna",
                "iau_designation": "(90377)",
                "object_type": ["Minor Planet", 0],
            }
        },
    )

    result = client.identify("Sedna")
    assert "Sedna" in result
    assert result["Sedna"]["permid"] == "90377"


@responses.activate
def test_identify_multiple(client):
    responses.get(
        IDENTIFIER_URL,
        json={
            "Ceres": {"found": 1, "permid": "1"},
            "2020 AB1": {"found": 1, "permid": None},
        },
    )

    result = client.identify(["Ceres", "2020 AB1"])
    assert "Ceres" in result
    assert "2020 AB1" in result



# --- PURE TESTS OF INPUT VALIDATION LOGIC (NO API CALLS) ------
#     These tests verify that the client raises appropriate
#     exceptions when given invalid input parameters.
# ---------------------------------------------------------------

def test_identify_empty_raises(client):
    with pytest.raises(MPCValidationError):
        client.identify([])


def test_identify_empty_string_raises(client):
    with pytest.raises(MPCValidationError):
        client.identify("")
