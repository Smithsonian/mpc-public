"""Tests for the Observatory Codes API."""

import pytest
import responses
import pandas as pd

from mpc_api import MPCClient


OBSCODES_URL = "https://data.minorplanetcenter.net/api/obscodes"


@pytest.fixture
def require_api(check_api):
    """Allow tests to skip if the Observatory Codes API is unreachable."""
    check_api(OBSCODES_URL)


# --- REAL TESTS THAT REALLY HIT THE API --------------
# -----------------------------------------------------

def test_get_observatory_real(require_api, client):
    """Hit the real API and verify observatory '500' (Geocentric) exists."""
    result = client.get_observatory("500")
    assert result["obscode"] == "500"
    assert result["name"] == "Geocentric"


def test_get_all_observatories_real(require_api, client):
    """Hit the real API and verify the full observatory list is returned."""
    result = client.get_all_observatories()
    assert isinstance(result, dict)
    assert "500" in result
    assert "F51" in result
    assert len(result) > 100


def test_get_all_observatories_df_real(require_api, client):
    """Hit the real API and verify the DataFrame format."""
    df = client.get_all_observatories_df()
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 100
    assert "name" in df.columns
    assert "500" in df.index


def test_search_observatories_real(require_api, client):
    """Hit the real API and search for 'Mauna'."""
    df = client.search_observatories("Mauna")
    assert isinstance(df, pd.DataFrame)
    assert len(df) >= 1
    assert "568" in df.index  # 568 is "Maunakea"



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
def test_get_observatory(client):
    responses.get(
        OBSCODES_URL,
        json={
            "obscode": "500",
            "name": "Geocentric",
            "longitude": 0.0,
            "rhocosphi": 0.0,
            "rhosinphi": 0.0,
            "observations_type": "optical",
        },
    )

    result = client.get_observatory("500")
    assert result["name"] == "Geocentric"


@responses.activate
def test_get_all_observatories(client):
    responses.get(
        OBSCODES_URL,
        json={
            "500": {"obscode": "500", "name": "Geocentric", "observations_type": "optical"},
            "F51": {"obscode": "F51", "name": "Pan-STARRS 1", "observations_type": "optical"},
        },
    )

    result = client.get_all_observatories()
    assert "500" in result
    assert "F51" in result


@responses.activate
def test_get_all_observatories_df(client):
    responses.get(
        OBSCODES_URL,
        json={
            "500": {"obscode": "500", "name": "Geocentric", "observations_type": "optical"},
            "F51": {"obscode": "F51", "name": "Pan-STARRS 1", "observations_type": "optical"},
        },
    )

    df = client.get_all_observatories_df()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert "name" in df.columns


@responses.activate
def test_search_observatories(client):
    responses.get(
        OBSCODES_URL,
        json={
            "568": {"obscode": "568", "name": "Mauna Kea", "observations_type": "optical"},
            "F51": {"obscode": "F51", "name": "Pan-STARRS 1, Haleakala", "observations_type": "optical"},
            "G96": {"obscode": "G96", "name": "Mt. Lemmon Survey", "observations_type": "optical"},
        },
    )

    df = client.search_observatories("Kea")
    assert len(df) == 1
    assert "568" in df.index
