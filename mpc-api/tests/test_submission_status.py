"""Tests for the Submission Status API."""

import pytest
import responses

from mpc_api import MPCClient, MPCValidationError, MPCNotFoundError


STATUS_URL = "https://data.minorplanetcenter.net/api/submission-status"


@pytest.fixture
def require_api(check_api):
    """Allow tests to skip if the Submission Status API is unreachable."""
    check_api(STATUS_URL)


# --- REAL TESTS THAT REALLY HIT THE API --------------
# -----------------------------------------------------

def test_get_submission_status_not_found_real(require_api, client):
    """Hit the real API with a fabricated submission ID.

    A non-existent submission ID should trigger a 404 and raise
    MPCNotFoundError.  This verifies that the API is reachable and
    the error handling path works end-to-end.
    """
    with pytest.raises(MPCNotFoundError):
        client.get_submission_status("1999-01-01T00:00:00.000_0000ZZZZ")



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
def test_get_submission_status_accepted(client):
    responses.get(
        STATUS_URL,
        json={
            "accepted": True,
            "pipeline_entry_time": "2026-01-01T00:06:00.696565+00:00",
            "fault_events": [],
        },
    )

    result = client.get_submission_status("2026-01-01T00:05:07.453_0000BhCE")
    assert result["accepted"] is True
    assert result["fault_events"] == []


@responses.activate
def test_get_submission_status_rejected(client):
    responses.get(
        STATUS_URL,
        json={
            "accepted": False,
            "pipeline_entry_time": None,
            "fault_events": [
                {"message": "exact duplicate", "phase": 2, "failure_code": 5}
            ],
        },
    )

    result = client.get_submission_status("2025-11-12T21:11:49.579_0000Ba8V")
    assert result["accepted"] is False
    assert len(result["fault_events"]) == 1


@responses.activate
def test_get_submission_status_not_found(client):
    responses.get(STATUS_URL, status=404)

    with pytest.raises(MPCNotFoundError):
        client.get_submission_status("2022-02-02T22:22:22.222_0000AaCC")



# --- PURE TESTS OF INPUT VALIDATION LOGIC (NO API CALLS) ------
#     These tests verify that the client raises appropriate
#     exceptions when given invalid input parameters.
# ---------------------------------------------------------------

def test_get_submission_status_empty_raises(client):
    with pytest.raises(MPCValidationError):
        client.get_submission_status("")
