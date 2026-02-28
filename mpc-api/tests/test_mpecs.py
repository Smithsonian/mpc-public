"""Tests for the MPECs API."""

import pytest
import responses

from mpc_api import MPCClient, MPCValidationError


MPECS_URL = "https://data.minorplanetcenter.net/api/mpecs"


@pytest.fixture
def require_api(check_api):
    """Allow tests to skip if the MPECs API is unreachable."""
    check_api(MPECS_URL)


# --- REAL TESTS THAT REALLY HIT THE API --------------
# -----------------------------------------------------

def test_get_mpecs_real(require_api, client):
    """Hit the real API for MPECs mentioning Apophis."""
    result = client.get_mpecs("Apophis")
    assert "Apophis" in result
    assert isinstance(result["Apophis"], list)
    assert len(result["Apophis"]) > 0
    mpec = result["Apophis"][0]
    assert "fullname" in mpec
    assert "title" in mpec
    assert "pubdate" in mpec
    assert "link" in mpec


def test_get_discovery_mpec_real(require_api, client):
    """Hit the real API and find the discovery MPEC for Apophis."""
    mpec = client.get_discovery_mpec("Apophis")
    assert mpec is not None
    assert "fullname" in mpec
    assert "pubdate" in mpec



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
def test_get_mpecs_single(client):
    responses.get(
        MPECS_URL,
        json={
            "Apophis": [
                {
                    "fullname": "2004-Y25",
                    "title": "2004 MN4",
                    "pubdate": "2004-12-20",
                    "link": "https://minorplanetcenter.net/mpec/K04/K04Y25.html",
                },
            ]
        },
    )

    result = client.get_mpecs("Apophis")
    assert "Apophis" in result
    assert len(result["Apophis"]) == 1


@responses.activate
def test_get_mpecs_multiple(client):
    responses.get(
        MPECS_URL,
        json={
            "Sedna": [{"fullname": "2003-V25", "title": "2003 VB12", "pubdate": "2003-11-15", "link": "link1"}],
            "Bennu": [{"fullname": "1999-S43", "title": "1999 RQ36", "pubdate": "1999-10-01", "link": "link2"}],
        },
    )

    result = client.get_mpecs(["Sedna", "Bennu"])
    assert "Sedna" in result
    assert "Bennu" in result


@responses.activate
def test_get_discovery_mpec(client):
    responses.get(
        MPECS_URL,
        json={
            "Bennu": [
                {"fullname": "2020-A01", "title": "Bennu update", "pubdate": "2020-01-01", "link": "link2"},
                {"fullname": "1999-S43", "title": "1999 RQ36", "pubdate": "1999-10-01", "link": "link1"},
            ]
        },
    )

    mpec = client.get_discovery_mpec("Bennu")
    assert mpec["fullname"] == "1999-S43"


@responses.activate
def test_get_discovery_mpec_not_found(client):
    responses.get(MPECS_URL, json={"unknown": []})

    result = client.get_discovery_mpec("unknown")
    assert result is None



# --- PURE TESTS OF INPUT VALIDATION LOGIC (NO API CALLS) ------
#     These tests verify that the client raises appropriate
#     exceptions when given invalid input parameters.
# ---------------------------------------------------------------

def test_get_mpecs_empty_raises(client):
    with pytest.raises(MPCValidationError):
        client.get_mpecs([])
