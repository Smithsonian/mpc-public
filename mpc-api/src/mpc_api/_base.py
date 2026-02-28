"""Shared HTTP logic for all API mixins."""

import requests

from .exceptions import MPCRequestError, MPCResponseError, MPCNotFoundError


BASE_URL = "https://data.minorplanetcenter.net"
SUBMIT_BASE_URL = "https://minorplanetcenter.net"


class BaseAPI:
    """Provides shared HTTP session and request helpers."""

    def __init__(self, *, api_key=None, timeout=60):
        self._session = requests.Session()
        self._session.headers["User-Agent"] = "mpc-api-python"
        self._timeout = timeout
        if api_key is not None:
            self._session.headers["Authorization"] = f"Bearer {api_key}"

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get(self, path, *, json=None, base_url=BASE_URL, **kwargs):
        """Send a GET request and return the parsed JSON response."""
        url = f"{base_url}{path}"
        try:
            resp = self._session.get(url, json=json, timeout=self._timeout, **kwargs)
        except requests.RequestException as exc:
            raise MPCRequestError(str(exc)) from exc
        return self._handle_response(resp)

    def _post(self, path, *, json=None, data=None, files=None,
              base_url=BASE_URL, **kwargs):
        """Send a POST request and return the parsed JSON response."""
        url = f"{base_url}{path}"
        try:
            resp = self._session.post(
                url, json=json, data=data, files=files,
                timeout=self._timeout, **kwargs,
            )
        except requests.RequestException as exc:
            raise MPCRequestError(str(exc)) from exc
        return self._handle_response(resp)

    def _post_raw(self, path, *, data=None, files=None,
                  base_url=BASE_URL, **kwargs):
        """Send a POST request and return the raw Response object."""
        url = f"{base_url}{path}"
        try:
            resp = self._session.post(
                url, data=data, files=files,
                timeout=self._timeout, **kwargs,
            )
        except requests.RequestException as exc:
            raise MPCRequestError(str(exc)) from exc
        if not resp.ok:
            self._raise_for_status(resp)
        return resp

    @staticmethod
    def _handle_response(resp):
        """Parse a JSON response, raising on HTTP errors."""
        if resp.status_code == 404:
            raise MPCNotFoundError(
                f"Not found (404): {resp.url}",
                status_code=404,
                response=resp,
            )
        if not resp.ok:
            raise MPCResponseError(
                f"HTTP {resp.status_code}: {resp.text[:200]}",
                status_code=resp.status_code,
                response=resp,
            )
        return resp.json()

    @staticmethod
    def _raise_for_status(resp):
        if resp.status_code == 404:
            raise MPCNotFoundError(
                f"Not found (404): {resp.url}",
                status_code=404,
                response=resp,
            )
        raise MPCResponseError(
            f"HTTP {resp.status_code}: {resp.text[:200]}",
            status_code=resp.status_code,
            response=resp,
        )
