"""Tests for the Check Near-Duplicates (CND) API."""

import pytest
import responses

from mpc_api import MPCClient, MPCValidationError


CND_URL = "https://data.minorplanetcenter.net/api/cnd"

SAMPLE_OBS = "f9671         C2020 02 21.46921410 05 10.27 +04 52 25.7          19.37oV~3n2UT08"


@pytest.fixture
def require_api(check_api):
    """Allow tests to skip if the CND API is unreachable."""
    check_api(CND_URL)


# --- REAL TESTS THAT REALLY HIT THE API --------------
# -----------------------------------------------------

def test_check_near_duplicates_real(require_api, client):
    """Hit the real CND API with the sample observation.

    We verify the response has the expected structure (a dict mapping
    the obs string to either a list of matches or a 'no results' string),
    without asserting a specific number of matches since the database
    content may change.
    """
    result = client.check_near_duplicates(SAMPLE_OBS)
    assert isinstance(result, dict)
    assert SAMPLE_OBS in result
    value = result[SAMPLE_OBS]
    if isinstance(value, list):
        for match in value:
            assert "obs80" in match


def test_count_near_duplicates_real(require_api, client):
    """Hit the real CND API and verify the count is a non-negative integer."""
    counts = client.count_near_duplicates(SAMPLE_OBS)
    assert isinstance(counts, dict)
    assert SAMPLE_OBS in counts
    assert isinstance(counts[SAMPLE_OBS], int)
    assert counts[SAMPLE_OBS] >= 0



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
def test_check_near_duplicates_match(client):
    responses.get(
        CND_URL,
        json={
            "request": {"obs": [SAMPLE_OBS]},
            "results": {
                SAMPLE_OBS: [
                    {
                        "angle_separation_arcsec": 0.021,
                        "obs80": SAMPLE_OBS,
                        "time_separation_s": 0.0,
                    }
                ]
            },
        },
    )

    result = client.check_near_duplicates(SAMPLE_OBS)
    assert SAMPLE_OBS in result
    assert len(result[SAMPLE_OBS]) == 1


@responses.activate
def test_check_near_duplicates_no_match(client):
    obs = "     abc123   C2020 03 23.46921410 05 13.27 +04 52 25.9          19.37oV     T08"
    responses.get(
        CND_URL,
        json={
            "request": {"obs": [obs]},
            "results": {
                obs: "No results returned which is strange; the search term should be in the database."
            },
        },
    )

    result = client.check_near_duplicates(obs)
    assert obs in result


@responses.activate
def test_count_near_duplicates(client):
    responses.get(
        CND_URL,
        json={
            "request": {"obs": [SAMPLE_OBS]},
            "results": {
                SAMPLE_OBS: [
                    {"obs80": SAMPLE_OBS, "time_separation_s": 0.0, "angle_separation_arcsec": 0.021},
                    {"obs80": "other_obs", "time_separation_s": 1.0, "angle_separation_arcsec": 2.0},
                ]
            },
        },
    )

    counts = client.count_near_duplicates(SAMPLE_OBS)
    assert counts[SAMPLE_OBS] == 2


@responses.activate
def test_count_near_duplicates_no_match(client):
    obs = "     abc123   C2020 03 23.46921410 05 13.27 +04 52 25.9          19.37oV     T08"
    responses.get(
        CND_URL,
        json={
            "request": {"obs": [obs]},
            "results": {obs: "No results"},
        },
    )

    counts = client.count_near_duplicates(obs)
    assert counts[obs] == 0



# --- PURE TESTS OF INPUT VALIDATION LOGIC (NO API CALLS) ------
#     These tests verify that the client raises appropriate
#     exceptions when given invalid input parameters.
# ---------------------------------------------------------------

def test_check_near_duplicates_empty_raises(client):
    with pytest.raises(MPCValidationError):
        client.check_near_duplicates([])


def test_check_near_duplicates_bad_time_raises(client):
    with pytest.raises(MPCValidationError, match="time_separation_s"):
        client.check_near_duplicates(SAMPLE_OBS, time_separation_s=100)


def test_check_near_duplicates_bad_angle_raises(client):
    with pytest.raises(MPCValidationError, match="angle_separation_arcsec"):
        client.check_near_duplicates(SAMPLE_OBS, angle_separation_arcsec=20)
