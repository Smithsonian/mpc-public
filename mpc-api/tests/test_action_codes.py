"""Tests for the Action Codes API."""

import pytest
import responses

from mpc_api import MPCClient, MPCValidationError


ACTION_URL = "https://data.minorplanetcenter.net/api/action-codes/retrieve"



# --- REAL TESTS THAT REALLY HIT THE API --------------
# NO REAL API TESTS for action codes.
# This endpoint triggers real emails to submitters when called.
# Real testing must be done manually.
# -----------------------------------------------------



# --- MOCKED TESTS THAT FAKE THE RETURNED API RESPONSE ---
#     In the tests below, we mock the expected API response, and then verify that
#     the MPCClient correctly handles/passes-through that response.
#
#     `@responses.activate` - intercepts all requests HTTP calls in this test
#      `responses.post(URL, json=[...])` -- registers a fake POST response
#
#     This allows us to test the client's handling of the API responses, without
#     relying on the actual API, which may be unavailable during testing.
# ---------------------------------------------------------

@responses.activate
def test_request_action_code(client):
    responses.post(
        ACTION_URL,
        json={"status": "ok", "message": "Action code email sent"},
    )

    result = client.request_action_code("2026-01-01T00:05:07.453_0000BhCE")
    assert "status" in result


@responses.activate
def test_request_action_code_with_trksub(client):
    responses.post(
        ACTION_URL,
        json={"status": "ok"},
    )

    result = client.request_action_code("ABC12345")
    assert result is not None



# --- PURE TESTS OF INPUT VALIDATION LOGIC (NO API CALLS) ------
#     These tests verify that the client raises appropriate
#     exceptions when given invalid input parameters.
# ---------------------------------------------------------------

def test_request_action_code_empty_raises(client):
    with pytest.raises(MPCValidationError):
        client.request_action_code("")
