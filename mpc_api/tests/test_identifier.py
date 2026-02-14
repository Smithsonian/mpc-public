"""Tests for the Designation Identifier API."""

import pytest
import responses

from mpc_api import MPCClient, MPCValidationError


IDENTIFIER_URL = "https://data.minorplanetcenter.net/api/query-identifier"


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


def test_identify_empty_raises(client):
    with pytest.raises(MPCValidationError):
        client.identify([])


def test_identify_empty_string_raises(client):
    with pytest.raises(MPCValidationError):
        client.identify("")
