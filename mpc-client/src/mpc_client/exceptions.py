"""Custom exception hierarchy for the MPC client."""

from __future__ import annotations

from typing import Any, Optional


class MPCAPIError(Exception):
    """Base exception for all MPC API errors."""


class MPCRequestError(MPCAPIError):
    """Network or timeout failure when making a request."""


class MPCResponseError(MPCAPIError):
    """Non-2xx HTTP status code returned by the API."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Any = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class MPCNotFoundError(MPCResponseError):
    """HTTP 404 — requested resource was not found."""


class MPCValidationError(MPCAPIError):
    """Local input validation failure before sending a request."""
