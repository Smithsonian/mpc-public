"""Tests for the Observatory Codes API."""

import responses
import pandas as pd

from mpc_api import MPCClient


OBSCODES_URL = "https://data.minorplanetcenter.net/api/obscodes"


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
