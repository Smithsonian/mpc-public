"""Tests for the MPECs API."""

import pytest
import responses

from mpc_api import MPCClient, MPCValidationError


MPECS_URL = "https://data.minorplanetcenter.net/api/mpecs"


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


def test_get_mpecs_empty_raises(client):
    with pytest.raises(MPCValidationError):
        client.get_mpecs([])
