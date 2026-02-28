"""Tests for the Observations API."""

import pytest
import responses
import pandas as pd

from mpc_api import MPCClient, MPCValidationError


OBS_URL = "https://data.minorplanetcenter.net/api/get-obs"


@pytest.fixture
def require_api(check_api):
    """Allow tests to skip if the Observations API is unreachable."""
    check_api(OBS_URL)


# --- REAL TESTS THAT REALLY HIT THE API --------------
# -----------------------------------------------------

def test_get_observations_obs80_real(require_api, client):
    """Hit the real API for Ceres observations in OBS80 format."""
    result = client.get_observations("Ceres", output_format="OBS80")
    assert "OBS80" in result
    assert isinstance(result["OBS80"], str)
    assert len(result["OBS80"]) > 0


def test_get_observations_xml_real(require_api, client):
    """Hit the real API for Ceres observations in XML format."""
    result = client.get_observations("Ceres", output_format="XML")
    assert "XML" in result
    assert "<optical>" in result["XML"]


def test_get_observations_df_real(require_api, client):
    """Hit the real API for Ceres observations as a DataFrame."""
    df = client.get_observations_df("Ceres")
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert "ra" in df.columns or "raStar" in df.columns



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
def test_get_observations_obs80(client):
    responses.get(
        OBS_URL,
        json=[{"OBS80": "     K99RQ36  C1999 09 11.12345 ..."}],
    )

    result = client.get_observations("Bennu", output_format="OBS80")
    assert "OBS80" in result


@responses.activate
def test_get_observations_xml(client):
    responses.get(
        OBS_URL,
        json=[{"XML": "<ades version='2022'>...</ades>"}],
    )

    result = client.get_observations("Bennu", output_format="XML")
    assert "XML" in result


@responses.activate
def test_get_observations_multiple_formats(client):
    responses.get(
        OBS_URL,
        json=[{
            "ADES_DF": [{"obsTime": "2023-01-01", "ra": 10.0, "dec": 20.0}],
            "OBS_DF": [{"date": "2023-01-01", "RA": "00 40 00.0", "Dec": "+20 00 00.0"}],
        }],
    )

    result = client.get_observations("Bennu", output_format=["ADES_DF", "OBS_DF"])
    assert "ADES_DF" in result
    assert "OBS_DF" in result


@responses.activate
def test_get_observations_df(client):
    responses.get(
        OBS_URL,
        json=[{
            "ADES_DF": [
                {"obsTime": "2023-01-01", "ra": 10.0, "dec": 20.0, "stn": "F51"},
                {"obsTime": "2023-01-02", "ra": 11.0, "dec": 21.0, "stn": "G96"},
            ]
        }],
    )

    df = client.get_observations_df("Bennu")
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert "ra" in df.columns



# --- PURE TESTS OF INPUT VALIDATION LOGIC (NO API CALLS) ------
#     These tests verify that the client raises appropriate
#     exceptions when given invalid input parameters.
# ---------------------------------------------------------------

def test_get_observations_empty_desig_raises(client):
    with pytest.raises(MPCValidationError):
        client.get_observations("")


def test_get_observations_invalid_format_raises(client):
    with pytest.raises(MPCValidationError, match="Invalid output_format"):
        client.get_observations("Bennu", output_format="INVALID")


def test_get_observations_df_invalid_fmt_raises(client):
    with pytest.raises(MPCValidationError, match="'ADES_DF' or 'OBS_DF'"):
        client.get_observations_df("Bennu", fmt="XML")
