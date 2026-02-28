"""Tests for MPCClient instantiation and basic properties."""

from mpc_api import MPCClient


def test_client_repr():
    client = MPCClient()
    assert repr(client) == "MPCClient()"


def test_client_has_all_methods():
    client = MPCClient()
    expected_methods = [
        "identify",
        "get_observatory",
        "get_all_observatories",
        "get_all_observatories_df",
        "search_observatories",
        "get_submission_status",
        "check_near_duplicates",
        "count_near_duplicates",
        "get_mpecs",
        "get_discovery_mpec",
        "get_observations",
        "get_observations_df",
        "get_neocp_observations",
        "get_neocp_observations_df",
        "get_orbit",
        "get_orbit_raw",
        "request_action_code",
        "submit_xml",
        "submit_psv",
    ]
    for method_name in expected_methods:
        assert hasattr(client, method_name), f"Missing method: {method_name}"
        assert callable(getattr(client, method_name))


def test_client_default_timeout():
    client = MPCClient()
    assert client._timeout == 60


def test_client_custom_timeout():
    client = MPCClient(timeout=120)
    assert client._timeout == 120
