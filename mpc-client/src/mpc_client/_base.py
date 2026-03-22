"""Shared HTTP logic for all API mixins."""

from __future__ import annotations

from typing import Any, Optional

import requests

from .exceptions import MPCRequestError, MPCResponseError, MPCNotFoundError


BASE_URL = "https://data.minorplanetcenter.net"
SUBMIT_BASE_URL = "https://minorplanetcenter.net"


class _MixinBase:
    """Declares HTTP methods provided by BaseAPI so mixins type-check correctly.

    All API mixin classes inherit from this stub.  At runtime the concrete
    implementations come from ``BaseAPI`` via MRO; these stubs exist only to
    give mypy enough information to resolve ``self._get`` / ``self._post`` /
    ``self._post_raw`` inside mixin methods.
    """

    def _get(self, path: str, **kwargs: Any) -> Any: ...

    def _post(self, path: str, **kwargs: Any) -> Any: ...

    def _post_raw(self, path: str, **kwargs: Any) -> Any: ...


class BaseAPI(_MixinBase):
    """Provides shared HTTP session and request helpers."""

    def __init__(self, *, api_key: Optional[str] = None, timeout: int = 60) -> None:
        self._session = requests.Session()
        self._session.headers["User-Agent"] = "mpc-client-python"
        self._timeout = timeout
        if api_key is not None:
            self._session.headers["Authorization"] = f"Bearer {api_key}"

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get(self, path: str, *, json: Any = None, base_url: str = BASE_URL, **kwargs: Any) -> Any:
        """Send a GET request and return the parsed JSON response."""
        url = f"{base_url}{path}"
        try:
            resp = self._session.get(url, json=json, timeout=self._timeout, **kwargs)
        except requests.RequestException as exc:
            raise MPCRequestError(str(exc)) from exc
        return self._handle_response(resp)

    def _post(self, path: str, *, json: Any = None, data: Any = None, files: Any = None,
              base_url: str = BASE_URL, **kwargs: Any) -> Any:
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

    def _post_raw(self, path: str, *, data: Any = None, files: Any = None,
                  base_url: str = BASE_URL, **kwargs: Any) -> requests.Response:
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
    def _handle_response(resp: requests.Response) -> Any:
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
    def _raise_for_status(resp: requests.Response) -> None:
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
