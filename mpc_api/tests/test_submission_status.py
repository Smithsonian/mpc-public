"""Tests for the Submission Status API."""

import pytest
import responses

from mpc_api import MPCClient, MPCValidationError, MPCNotFoundError


STATUS_URL = "https://data.minorplanetcenter.net/api/submission-status"


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


def test_get_submission_status_empty_raises(client):
    with pytest.raises(MPCValidationError):
        client.get_submission_status("")
