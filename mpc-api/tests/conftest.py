"""Shared fixtures and helpers for mpc_api tests."""

import pytest
import requests

from mpc_api import MPCClient


@pytest.fixture
def client():
    """Return an MPCClient instance for testing."""
    return MPCClient()


@pytest.fixture
def check_api():
    """Fixture that returns a helper to skip tests if API URLs are unreachable.

    Usage in test files::

        @pytest.fixture
        def require_api(check_api):
            check_api(MY_URL)

    A bare GET that returns any status other than 404 is treated as
    "available" (POST-only endpoints may return 405 or 501, which is
    fine — it proves the route exists).  Only connection-level failures
    and 404 trigger a skip.
    """
    def _check(*urls):
        for url in urls:
            try:
                resp = requests.get(url, timeout=5)
            except requests.RequestException:
                pytest.skip(f"API unavailable: {url}")
            if resp.status_code == 404:
                pytest.skip(f"API unavailable: {url}")
    return _check
