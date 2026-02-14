"""Tests for the Action Codes API."""

import pytest
import responses

from mpc_api import MPCClient, MPCValidationError


ACTION_URL = "https://data.minorplanetcenter.net/api/action-codes/retrieve"


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


def test_request_action_code_empty_raises(client):
    with pytest.raises(MPCValidationError):
        client.request_action_code("")
