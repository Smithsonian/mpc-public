"""Tests for the NEOCP Observations API."""

import pytest
import requests
import responses
import pandas as pd

from mpc_api import MPCClient, MPCValidationError


NEOCP_URL = "https://data.minorplanetcenter.net/api/get-obs-neocp"
TABULAR_URL = "https://minorplanetcenter.net/iau/NEO/toconfirm_tabular.html"



# --- REAL TESTS THAT REALLY HIT THE API --------------
# -----------------------------------------------------
@pytest.fixture
def require_api(check_api):
    """Allow tests to skip if the NEOCP API or tabular page is unreachable."""
    check_api(NEOCP_URL)
    # TABULAR_URL must return 200 (it's a regular HTML page, not a POST endpoint)
    try:
        resp = requests.get(TABULAR_URL, timeout=5)
        resp.raise_for_status()
    except requests.RequestException:
        pytest.skip(f"API unavailable: {TABULAR_URL}")

def grab_neocp_trksub():
    """Grab a real `trksub` value from the MPC's NEOCP tabular page."""
    return pd.read_html(TABULAR_URL)[0].iloc[0]['Temp Desig']

def test_get_neocp_observations_obs80_real(require_api, client):
    """This test actually hits the real API, and verifies that
    the returned OBS80 string starts with the expected `trksub` value."""
    trksub = grab_neocp_trksub()
    result = client.get_neocp_observations(trksub, output_format="OBS80")
    assert "OBS80" in result and result["OBS80"].startswith("     " + trksub)

def test_get_neocp_observations_xml_real(require_api, client):
    """This test actually hits the real API, and verifies that
    the returned XML string contains the expected `<optical>` tag."""
    trksub = grab_neocp_trksub()
    result = client.get_neocp_observations(trksub, output_format="XML")
    assert "XML" in result and "<optical>" in result["XML"]

def test_get_neocp_observations_df_real(require_api, client):
    """This test actually hits the real API, and verifies that
    the returned DataFrame contains a 'trksub' column, and that all rows have
    the expected `trksub` value."""
    trksub = grab_neocp_trksub()
    df = client.get_neocp_observations_df(trksub)
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert "trksub" in df.columns and (df["trksub"] == trksub).all()



# --- MOCKED TESTS THAT FAKE THE RETURNED API RESPONSE ---
#     In the tests below, we mock the expected API response, and then verify that
#     the MPCClient correctly handles/passes-through that response.
#
#     `@responses.activate` - intercepts all requests HTTP calls in this test
#      `responses.get(NEOCP_URL, json=[...])` — registers a fake GET response
#
#     This allows us to test the client's handling of the API responses, without relying on the actual API,
#     which may be unavailable during testing.
# --------------------------------------------------------

@responses.activate
def test_get_neocp_observations_obs80(client):
    """ This test verifies that when the API returns an OBS80 string, the client correctly extracts and returns it.
    """
    responses.get(
        NEOCP_URL,
        json=[{"OBS80": "     P21Eetc  C2025 02 10.12345 ..."}],
    )

    result = client.get_neocp_observations("P21Eetc", output_format="OBS80")
    assert "OBS80" in result and result["OBS80"].startswith("     P21Eetc")


@responses.activate
def test_get_neocp_observations_xml(client):
    """ This test verifies that when the API returns an XML string, the client correctly extracts and returns it."""
    responses.get(
        NEOCP_URL,
        json=[{"XML": "<ades version='2022'>...</ades>"}],
    )

    result = client.get_neocp_observations("P21Eetc", output_format="XML")
    assert "XML" in result


@responses.activate
def test_get_neocp_observations_df(client):
    """ This test verifies that when the API returns a JSON response with an 'ADES_DF' key, the client correctly converts it to a DataFrame."""
    responses.get(
        NEOCP_URL,
        json=[{
            "ADES_DF": [
                {"trksub": "P21Eetc", "obstime": "2025-02-10", "ra": 10.0, "dec": 20.0, "stn": "F51"},
                {"trksub": "P21Eetc", "obstime": "2025-02-11", "ra": 11.0, "dec": 21.0, "stn": "G96"},
            ]
        }],
    )

    df = client.get_neocp_observations_df("P21Eetc")
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2


# --- PURE TESTS OF INPUT VALIDATION LOGIC (NO API CALLS) ------
#     These tests verify that the client raises appropriate
#     exceptions when given invalid input parameters.
# --------------------------------------------------------------

def test_get_neocp_observations_empty_raises(client):
    """ This test verifies that calling `get_neocp_observations` with an empty string raises an MPCValidationError."""
    with pytest.raises(MPCValidationError):
        client.get_neocp_observations("")


def test_get_neocp_observations_invalid_format_raises(client):
    """This test verifies that calling `get_neocp_observations` with an invalid output_format raises an MPCValidationError."""
    with pytest.raises(MPCValidationError, match="Invalid output_format"):
        client.get_neocp_observations("P21Eetc", output_format="INVALID")


def test_get_neocp_observations_df_invalid_fmt_raises(client):
    """This test verifies that calling `get_neocp_observations_df` with an invalid format raises an MPCValidationError."""
    with pytest.raises(MPCValidationError, match="'ADES_DF' or 'OBS_DF'"):
        client.get_neocp_observations_df("P21Eetc", fmt="XML")


