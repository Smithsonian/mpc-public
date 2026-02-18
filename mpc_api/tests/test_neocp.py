"""Tests for the NEOCP Observations API."""

import pytest
import responses
import pandas as pd

from mpc_api import MPCClient, MPCValidationError


NEOCP_URL = "https://data.minorplanetcenter.net/api/get-obs-neocp"


@responses.activate
def test_get_neocp_observations_obs80(client):
    responses.get(
        NEOCP_URL,
        json=[{"OBS80": "     P21Eetc  C2025 02 10.12345 ..."}],
    )

    result = client.get_neocp_observations("P21Eetc", output_format="OBS80")
    assert "OBS80" in result


@responses.activate
def test_get_neocp_observations_xml(client):
    responses.get(
        NEOCP_URL,
        json=[{"XML": "<ades version='2022'>...</ades>"}],
    )

    result = client.get_neocp_observations("P21Eetc", output_format="XML")
    assert "XML" in result


@responses.activate
def test_get_neocp_observations_df(client):
    responses.get(
        NEOCP_URL,
        json=[{
            "ADES_DF": [
                {"trksub": "P21Eetc", "obstime": "2025-02-10", "ra": 10.0, "dec": 20.0, "stn": "F51"},
                {"trksub": "P21Eetc", "obstime": "2025-02-11", "ra": 11.0, "dec": 21.0, "stn": "G96"},
            ]
        }],
    )

    df = client.get_neocp_observations_df("P21Eetc")
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2


def test_get_neocp_observations_empty_raises(client):
    with pytest.raises(MPCValidationError):
        client.get_neocp_observations("")


def test_get_neocp_observations_invalid_format_raises(client):
    with pytest.raises(MPCValidationError, match="Invalid output_format"):
        client.get_neocp_observations("P21Eetc", output_format="INVALID")


def test_get_neocp_observations_df_invalid_fmt_raises(client):
    with pytest.raises(MPCValidationError, match="'ADES_DF' or 'OBS_DF'"):
        client.get_neocp_observations_df("P21Eetc", fmt="XML")
