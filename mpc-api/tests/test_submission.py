"""Tests for the Submission API."""

import os
import tempfile

import pytest
import responses

from mpc_api import MPCClient, MPCValidationError, MPCResponseError


XML_TEST_URL = "https://minorplanetcenter.net/submit_xml_test"
PSV_TEST_URL = "https://minorplanetcenter.net/submit_psv_test"
XML_PROD_URL = "https://minorplanetcenter.net/submit_xml"
PSV_PROD_URL = "https://minorplanetcenter.net/submit_psv"


SAMPLE_XML = '<?xml version="1.0"?><ades version="2022"><optical></optical></ades>'



# --- REAL TESTS THAT REALLY HIT THE API --------------
# NO REAL API TESTS for submissions.
# These endpoints actually submit observation data to the MPC pipeline
# (even the _test endpoints trigger processing).  Real submission
# testing must be done manually with valid ADES data and a known
# submitter account.
# -----------------------------------------------------



# --- MOCKED TESTS THAT FAKE THE RETURNED API RESPONSE ---
#     In the tests below, we mock the expected API response, and then verify that
#     the MPCClient correctly handles/passes-through that response.
#
#     `@responses.activate` - intercepts all requests HTTP calls in this test
#      `responses.post(URL, ...)` -- registers a fake POST response
#
#     This allows us to test the client's handling of the API responses, without
#     relying on the actual API, which may be unavailable during testing.
# ---------------------------------------------------------

@responses.activate
def test_submit_xml_test(client):
    responses.post(
        XML_TEST_URL,
        body="[My ack].  Submission ID is 2026-02-09T11:42:17.655_00000FrY",
        status=200,
    )

    result = client.submit_xml(
        SAMPLE_XML, ack="My ack", ac2="test@example.com", test=True,
    )
    assert result["status_code"] == 200
    assert "Submission ID" in result["message"]


@responses.activate
def test_submit_psv_test(client):
    responses.post(
        PSV_TEST_URL,
        body="[My ack].  Submission ID is 2026-02-09T11:42:17.976_00000FrZ",
        status=200,
    )

    result = client.submit_psv(
        "# version=2022\nsome psv data",
        ack="My ack",
        ac2="test@example.com",
        test=True,
    )
    assert result["status_code"] == 200


@responses.activate
def test_submit_xml_production(client):
    responses.post(
        XML_PROD_URL,
        body="[My ack].  Submission ID is 2026-02-09T11:42:18.000_00000FrA",
        status=200,
    )

    result = client.submit_xml(
        SAMPLE_XML, ack="My ack", ac2="test@example.com", test=False,
    )
    assert result["status_code"] == 200


@responses.activate
def test_submit_xml_from_file(client):
    responses.post(XML_TEST_URL, body="[ok]. Submission ID is xxx", status=200)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".xml", delete=False) as f:
        f.write(SAMPLE_XML)
        f.flush()
        filepath = f.name

    try:
        result = client.submit_xml(
            filepath, ack="My ack", ac2="test@example.com",
        )
        assert result["status_code"] == 200
    finally:
        os.unlink(filepath)


@responses.activate
def test_submit_xml_missing_ack_returns_400(client):
    responses.post(XML_TEST_URL, body="error: no `ack` value provided", status=400)

    with pytest.raises(MPCResponseError):
        client.submit_xml(
            SAMPLE_XML, ack="ack", ac2="test@example.com",
        )


@responses.activate
def test_submit_xml_with_obj_type(client):
    responses.post(XML_TEST_URL, body="[ack]. Submission ID is xxx", status=200)

    result = client.submit_xml(
        SAMPLE_XML,
        ack="My ack",
        ac2="test@example.com",
        obj_type="NEO",
    )
    assert result["status_code"] == 200
    # Verify obj_type was sent in the request
    assert "obj_type" in responses.calls[0].request.body.decode()



# --- PURE TESTS OF INPUT VALIDATION LOGIC (NO API CALLS) ------
#     These tests verify that the client raises appropriate
#     exceptions when given invalid input parameters.
# ---------------------------------------------------------------

def test_submit_xml_empty_ack_raises(client):
    with pytest.raises(MPCValidationError, match="ack"):
        client.submit_xml(SAMPLE_XML, ack="", ac2="test@example.com")


def test_submit_xml_empty_ac2_raises(client):
    with pytest.raises(MPCValidationError, match="ac2"):
        client.submit_xml(SAMPLE_XML, ack="My ack", ac2="")
