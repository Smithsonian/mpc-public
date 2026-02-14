"""Shared fixtures for mpc_api tests."""

import pytest
from mpc_api import MPCClient


@pytest.fixture
def client():
    """Return an MPCClient instance for testing."""
    return MPCClient()
