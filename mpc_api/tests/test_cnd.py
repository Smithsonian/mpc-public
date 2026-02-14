"""Tests for the Check Near-Duplicates (CND) API."""

import pytest
import responses

from mpc_api import MPCClient, MPCValidationError


CND_URL = "https://data.minorplanetcenter.net/api/cnd"

SAMPLE_OBS = "f9671         C2020 02 21.46921410 05 10.27 +04 52 25.7          19.37oV~3n2UT08"


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


def test_check_near_duplicates_empty_raises(client):
    with pytest.raises(MPCValidationError):
        client.check_near_duplicates([])


def test_check_near_duplicates_bad_time_raises(client):
    with pytest.raises(MPCValidationError, match="time_separation_s"):
        client.check_near_duplicates(SAMPLE_OBS, time_separation_s=100)


def test_check_near_duplicates_bad_angle_raises(client):
    with pytest.raises(MPCValidationError, match="angle_separation_arcsec"):
        client.check_near_duplicates(SAMPLE_OBS, angle_separation_arcsec=20)
