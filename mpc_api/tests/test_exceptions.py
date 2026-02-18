"""Tests for the exception hierarchy."""

from mpc_api import (
    MPCAPIError,
    MPCRequestError,
    MPCResponseError,
    MPCNotFoundError,
    MPCValidationError,
)


def test_hierarchy():
    assert issubclass(MPCRequestError, MPCAPIError)
    assert issubclass(MPCResponseError, MPCAPIError)
    assert issubclass(MPCNotFoundError, MPCResponseError)
    assert issubclass(MPCValidationError, MPCAPIError)


def test_response_error_attributes():
    err = MPCResponseError("bad", status_code=400, response="resp")
    assert err.status_code == 400
    assert err.response == "resp"
    assert str(err) == "bad"


def test_not_found_error_attributes():
    err = MPCNotFoundError("missing", status_code=404)
    assert err.status_code == 404
    assert isinstance(err, MPCResponseError)
