"""Tests for wis.obscodes."""

# Third-party imports
import contextlib
import os
import time
from pathlib import Path
from typing import Never

import numpy as np
import pytest

# Local imports
from wis.obscodes import MPCObsCodes


def test_MPCObsCodes__local_obscode_file_is_stale(tmp_path: Path) -> None:
    """Test that the _local_obscode_file_is_stale function behaves as expected."""
    # Create an uninitialized instance, skipping the normal constructor initialization
    M = MPCObsCodes.__new__(MPCObsCodes)

    # Overwrite the local_obscode_file attribute & test that this file does NOT yet exist
    M.local_obscode_file = tmp_path / "test_obscode.json"
    with contextlib.suppress(Exception):
        os.remove(M.local_obscode_file)
    assert not os.path.isfile(M.local_obscode_file)

    # Test that `_local_obscode_file_is_stale` returns True when the file does not exist
    assert M._local_obscode_file_is_stale()

    # Write an empty dict to the file
    M._write_local_obscode_file({}, {})
    assert os.path.isfile(M.local_obscode_file)

    # Test that `_local_obscode_file_is_stale` returns False when the file exists (and is new)
    assert not M._local_obscode_file_is_stale()


def test_MPCObsCodes__read_and_write_local_obscode_file(tmp_path: Path) -> None:
    """Test that the _read_local_obscode_file & _write_local_obscode_file functions behave as expected."""
    # Create an uninitialized instance, skipping the normal constructor initialization
    M = MPCObsCodes.__new__(MPCObsCodes)

    # Overwrite the local_obscode_file attribute & test that this file does NOT yet exist
    M.local_obscode_file = tmp_path / "test_obscode.json"
    assert not os.path.isfile(M.local_obscode_file)

    # Write a dict to the file
    in_dict = {
        "GeocentricXYZ": {"Z49": np.array([0.59128664, -0.02678492, 0.803336])},
        "TwoLine": {"C54": True},
    }
    M._write_local_obscode_file(in_dict["GeocentricXYZ"], in_dict["TwoLine"])
    assert os.path.isfile(M.local_obscode_file)

    # Read from the file
    GeocentricXYZ, TwoLine = M._read_local_obscode_file()
    for k, v in in_dict["GeocentricXYZ"].items():
        assert k in GeocentricXYZ, "Output dict not as expected"
        assert np.array_equal(v, GeocentricXYZ[k]), "Output dict-array not as expected"
    for k, v in in_dict["TwoLine"].items():
        assert k in TwoLine, "Output dict not as expected"
        assert v == TwoLine[k], "Output dict not as expected"


@pytest.mark.integration
def test_MPCObsCodes_query_obscodes_api() -> None:
    """Test that the query_obscodes_api function behaves as expected.

    Tests the MPC REST API integration.
    """
    # Create an uninitialized instance, skipping the normal constructor initialization
    M = MPCObsCodes.__new__(MPCObsCodes)

    # Read from the API
    GeocentricXYZ, TwoLine = M.query_obscodes_api()
    assert len(GeocentricXYZ) > 1000, "Expected >1000 obscodes, but got fewer"
    assert 2 < len(TwoLine) < 200, "Expected >2 & < 200 obscodes"


def test_MPCObsCodes_get_geocentric_xyz_dict(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that the get_geocentric_xyz_dict function behaves as expected (with fallback=False)."""
    # MonkeyPatch the query_obscodes_api method to return a known dict
    GeocentricXYZ = {"test": "test"}
    TwoLine = {"test": "test"}

    def mock_query_obscodes_api(
        self: MPCObsCodes,
    ) -> tuple[dict[str, str], dict[str, str]]:
        return GeocentricXYZ, TwoLine

    monkeypatch.setattr(MPCObsCodes, "query_obscodes_api", mock_query_obscodes_api)

    # Create an uninitialized instance, skipping the normal constructor initialization
    M = MPCObsCodes.__new__(MPCObsCodes)

    # Read from the database using get_geocentric_xyz_dict
    # NB: We force fallback=False, save_local=False to avoid reading-from or writing-to the local file
    a, b = M.get_geocentric_xyz_dict(fallback=False, save_local=False)
    assert a == GeocentricXYZ, "Output dict not as expected"
    assert b == TwoLine, "Output dict not as expected"


def test_MPCObsCodes_get_geocentric_xyz_dict_nodbaccess(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Test that the get_geocentric_xyz_dict function behaves as expected when it can't access the database."""

    # MonkeyPatch the query_obscodes_api method to raise an exception
    def mock_query_obscodes_api(self: MPCObsCodes) -> Never:
        raise Exception("Test exception")

    monkeypatch.setattr(MPCObsCodes, "query_obscodes_api", mock_query_obscodes_api)

    # Create an uninitialized instance, skipping the normal constructor initialization
    M = MPCObsCodes.__new__(MPCObsCodes)

    # Overwrite the local_obscode_file attribute & test that this file does NOT yet exist
    M.local_obscode_file = tmp_path / "test_obscode.json"
    assert not os.path.isfile(M.local_obscode_file)

    # Write a dict to the file
    in_dict = {
        "GeocentricXYZ": {"Z49": np.array([0.59128664, -0.02678492, 0.803336])},
        "TwoLine": {"C54": True},
    }
    M._write_local_obscode_file(in_dict["GeocentricXYZ"], in_dict["TwoLine"])
    assert os.path.isfile(M.local_obscode_file)

    # Read from the database using get_geocentric_xyz_dict
    GeocentricXYZ, TwoLine = M.get_geocentric_xyz_dict(fallback=True, save_local=False)
    for k, v in in_dict["GeocentricXYZ"].items():
        assert k in GeocentricXYZ, "Output dict not as expected"
        assert np.array_equal(v, GeocentricXYZ[k]), "Output dict-array not as expected"
    for k, v in in_dict["TwoLine"].items():
        assert k in TwoLine, "Output dict not as expected"
        assert v == TwoLine[k], "Output dict not as expected"


def test_MPCObsCodes_get_geocentric_xyz_dict_savelocal(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Test that the get_geocentric_xyz_dict function saves to file when desired."""
    # MonkeyPatch the query_obscodes_api method to return a known dict
    GeocentricXYZ = {"Z49": np.array([0.59128664, -0.02678492, 0.803336])}
    TwoLine = {"C54": True}

    def mock_query_obscodes_api(
        self: MPCObsCodes,
    ) -> tuple[dict[str, np.ndarray], dict[str, bool]]:
        return GeocentricXYZ, TwoLine

    monkeypatch.setattr(MPCObsCodes, "query_obscodes_api", mock_query_obscodes_api)

    # Create an uninitialized instance, skipping the normal constructor initialization
    M = MPCObsCodes.__new__(MPCObsCodes)

    # Overwrite the local_obscode_file attribute & test that this file does NOT yet exist
    M.local_obscode_file = tmp_path / "test_obscode.json"
    assert not os.path.isfile(M.local_obscode_file)

    # Read from the database using get_geocentric_xyz_dict
    # Because there is no local file, the function should write to the file
    a, b = M.get_geocentric_xyz_dict(fallback=False, save_local=True)
    assert set(a.keys()) == set(
        GeocentricXYZ.keys()
    ), "Keys mismatch in geocentric dict"
    for k, v in GeocentricXYZ.items():
        assert np.array_equal(v, a[k]), f"Array mismatch for key {k}"
    assert b == TwoLine, "TwoLine dict not as expected"

    assert os.path.isfile(M.local_obscode_file), "Local file not created"


def test_MPCObsCodes_init(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Test that the MPCObsCodes class initializes as expected."""
    # MonkeyPatch the query_obscodes_api method to return a known dict
    GeocentricXYZ = {"Z49": np.array([0.59128664, -0.02678492, 0.803336])}
    TwoLine = {"C54": True}

    def mock_query_obscodes_api(
        self: MPCObsCodes,
    ) -> tuple[dict[str, np.ndarray], dict[str, bool]]:
        return GeocentricXYZ, TwoLine

    monkeypatch.setattr(MPCObsCodes, "query_obscodes_api", mock_query_obscodes_api)
    # MonkeyPatch the local_obscode_file to a temporary path to avoid system cache
    temp_file = tmp_path / "obscode.json"
    monkeypatch.setattr(MPCObsCodes, "local_obscode_file", temp_file)

    # Initialize the class
    M = MPCObsCodes()

    # Check that the geocentric_xyz_dict attribute is as expected
    assert hasattr(M, "geocentric_xyz_dict"), "Attribute not found"
    assert hasattr(M, "two_line_dict"), "Attribute not found"
    # Compare geocentric_xyz_dict
    for k, v in GeocentricXYZ.items():
        assert k in M.geocentric_xyz_dict, f"Key {k} missing in geocentric_xyz_dict"
        assert np.array_equal(
            v, M.geocentric_xyz_dict[k]
        ), f"Array mismatch for key {k}"
    # Compare two_line_dict
    assert M.two_line_dict == TwoLine, "TwoLine dict not as expected"


@pytest.mark.parametrize(
    "file_state, fallback, expected_api_calls, expected_data_source",
    [
        ("fresh", True, 0, "local"),
        ("fresh", False, 1, "api"),
        ("stale", True, 1, "api"),
        ("stale", False, 1, "api"),
        ("none", True, 1, "api"),
    ],
)
def test_MPCObsCodes_get_geocentric_xyz_dict_staleness(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    file_state: str,
    fallback: bool,
    expected_api_calls: int,
    expected_data_source: str,
) -> None:
    """Test that get_geocentric_xyz_dict uses local file when not stale and API when stale."""
    # Create test data
    local_data = {"Z49": np.array([0.59128664, -0.02678492, 0.803336])}
    local_twoline = {"C54": True}
    api_data = {"W84": np.array([0.12345678, -0.87654321, 0.55555555])}
    api_twoline = {"C55": True}

    # Track API calls
    api_called = []

    def mock_query_obscodes_api(
        self: MPCObsCodes,
    ) -> tuple[dict[str, np.ndarray], dict[str, bool]]:
        api_called.append(True)
        return api_data, api_twoline

    monkeypatch.setattr(MPCObsCodes, "query_obscodes_api", mock_query_obscodes_api)

    # Create an uninitialized instance
    M = MPCObsCodes.__new__(MPCObsCodes)
    M.local_obscode_file = tmp_path / "test_obscode.json"

    # Set up file state based on parameter
    if file_state == "fresh":
        M._write_local_obscode_file(local_data, local_twoline)
        assert os.path.isfile(M.local_obscode_file)
        assert not M._local_obscode_file_is_stale()
    elif file_state == "stale":
        M._write_local_obscode_file(local_data, local_twoline)
        assert os.path.isfile(M.local_obscode_file)
        # Make file stale by setting modification time to 2 days ago
        stale_time = time.time() - (2 * 24 * 3600)
        os.utime(M.local_obscode_file, (stale_time, stale_time))
        assert M._local_obscode_file_is_stale()
    elif file_state == "none":
        # Ensure no file exists
        if os.path.isfile(M.local_obscode_file):
            os.remove(M.local_obscode_file)
        assert not os.path.isfile(M.local_obscode_file)
        assert M._local_obscode_file_is_stale()
    else:
        raise ValueError(f"Unknown file_state: {file_state}")

    # Clear API call tracking before test
    api_called.clear()

    # Get data with specified parameters
    GeocentricXYZ, TwoLine = M.get_geocentric_xyz_dict(
        fallback=fallback, save_local=False
    )

    # Verify API call count matches expectation
    assert (
        len(api_called) == expected_api_calls
    ), f"API should be called {expected_api_calls} time(s) for file_state={file_state}, fallback={fallback}"

    # Verify data source matches expectation
    if expected_data_source == "local":
        assert list(GeocentricXYZ.keys()) == list(
            local_data.keys()
        ), f"Should use local data when file_state={file_state}, fallback={fallback}"
        for key in local_data:
            assert np.array_equal(
                GeocentricXYZ[key], local_data[key]
            ), f"Should use local data for {key} when file_state={file_state}, fallback={fallback}"
        assert (
            TwoLine == local_twoline
        ), f"Should use local two-line data when file_state={file_state}, fallback={fallback}"
    else:  # expected_data_source == "api"
        assert list(GeocentricXYZ.keys()) == list(
            api_data.keys()
        ), f"Should use API data when file_state={file_state}, fallback={fallback}"
        for key in api_data:
            assert np.array_equal(
                GeocentricXYZ[key], api_data[key]
            ), f"Should use API data for {key} when file_state={file_state}, fallback={fallback}"
        assert (
            TwoLine == api_twoline
        ), f"Should use API two-line data when file_state={file_state}, fallback={fallback}"
