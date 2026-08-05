"""Tests for the KernelSpecifier class.

*** NB Data downloads are NOT tested here, as it requires internet access
*** See test_integration_kernels_downloads.py for this

"""

# Third-party imports
# -----------------------------------------
import json
import os
from datetime import datetime
from pathlib import Path

import pytest
import spiceypy as sp

# Local imports
# -----------------------------------------
from wis.kernelspecifier import KernelSpecifier

# Test Fixtures
# -----------------------------------------


@pytest.fixture
def minimal_kernel_specifier(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> KernelSpecifier:
    """Create a minimal KernelSpecifier instance for testing."""
    # MonkeyPatch data_dir to use tmp_path
    monkeypatch.setattr("wis.constants.Directories.data_dir", tmp_path)

    KS = KernelSpecifier(
        obscodeMPC="000",
        obscodeJPL="000",
        name="Test Observatory",
        files=["https://example.com/test.tls"],
        wildcards={},
        timecritical=[],
    )
    return KS


@pytest.fixture
def kernel_specifier_with_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> KernelSpecifier:
    """Create KernelSpecifier with file specifications."""
    # MonkeyPatch data_dir to use tmp_path
    monkeypatch.setattr("wis.constants.Directories.data_dir", tmp_path)

    KS = KernelSpecifier(
        obscodeMPC="000",
        obscodeJPL="000",
        name="Test Observatory",
        files=["https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0012.tls"],
        wildcards={},
        timecritical=[],
    )
    return KS


@pytest.fixture
def kernel_specifier_with_wildcards(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> KernelSpecifier:
    """Create KernelSpecifier with wildcard file specifications."""
    # MonkeyPatch data_dir to use tmp_path
    monkeypatch.setattr("wis.constants.Directories.data_dir", tmp_path)

    KS = KernelSpecifier(
        obscodeMPC="000",
        obscodeJPL="000",
        name="Test Observatory",
        files=[
            "https://archive.stsci.edu/missions/tess/models/tess2018338154429-41241_de430.bsp"
        ],
        wildcards={"https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/": "*.tls"},
        timecritical=[],
    )
    return KS


# Test Functions
# -----------------------------------------


# =============================================================================
# Constructor & Basic Attributes
# =============================================================================


def test_KernelSpecifier_constructor_validation() -> None:
    """Test that KernelSpecifier constructor validates required parameters."""
    # This would test validation logic - currently not implemented
    pass


def test_KernelSpecifier_constructor_attributes(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Test that KernelSpecifier constructor correctly sets attributes."""
    # MonkeyPatch data_dir method on `Directories` and hence on `KernelSpecifier`
    monkeypatch.setattr("wis.constants.Directories.data_dir", tmp_path)

    TestKS = KernelSpecifier(
        obscodeMPC="GROUND430",
        obscodeJPL="GROUND430",
        name="GROUND430",
        files=[
            "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/latest_leapseconds.tls"
        ],
        wildcards={},
    )

    # Check the attributes are as expected
    # Note: data_dir is not directly accessible on Pydantic model, but download_subdir uses it
    assert TestKS.obscodeJPL == "GROUND430", "obscode not as expected"
    assert TestKS.obscodeMPC == "GROUND430", "obscode not as expected"
    assert TestKS.name == "GROUND430", "name not as expected"
    assert TestKS.download_subdir == os.path.join(
        tmp_path, TestKS.obscodeJPL
    ), "download_subdir not as expected"
    assert TestKS.files == [
        "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/latest_leapseconds.tls"
    ], "files not as expected"
    assert TestKS.wildcards == {}, "wildcards not as expected"
    assert TestKS.timecritical == [], "timecritical not as expected"
    assert TestKS.kernel_filepath_map == {
        os.path.join(
            TestKS.download_subdir, "latest_leapseconds.tls"
        ): "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/latest_leapseconds.tls"
    }, "expected_local_kernel_filepaths not as expected"

    expected_kernel_filepath_map_json = os.path.join(
        TestKS.download_subdir, "kernel_filepath_map.json"
    )
    assert os.path.isfile(
        expected_kernel_filepath_map_json
    ), f"{expected_kernel_filepath_map_json} does not exist"
    os.remove(expected_kernel_filepath_map_json)
    assert not os.path.isfile(expected_kernel_filepath_map_json)


# =============================================================================
# Filepath Map Generation
# =============================================================================


def test_generate_kernel_filepath_map_with_explicit_files(
    kernel_specifier_with_files: KernelSpecifier,
) -> None:
    """Test that generate_kernel_filepath_map works with explicit file URLs."""
    KS = kernel_specifier_with_files

    # Check the json file does not exist
    assert not os.path.isfile(
        KS.kernel_json
    ), f"{KS.kernel_json} should not exist at this point, but it does"

    # Call the method to generate the kernel_filepath_map
    kernel_filepath_map = KS.generate_kernel_filepath_map()

    # Assert that the kernel_filepath_map is as expected
    assert (
        len(kernel_filepath_map) == 1
    ), f"Expected 1 filepath, but got {len(kernel_filepath_map)}"
    assert os.path.isfile(KS.kernel_json), f"{KS.kernel_json} does not exist"


def test_generate_kernel_filepath_map_with_wildcards(
    monkeypatch: pytest.MonkeyPatch, kernel_specifier_with_wildcards: KernelSpecifier
) -> None:
    """Test that generate_kernel_filepath_map works with wildcard file URLs."""
    KS = kernel_specifier_with_wildcards

    # MonkeyPatch the method `_listFD` on `KernelSpecifier`
    def mock_listFD(self: KernelSpecifier, url: str, wildcard: str = "") -> list[str]:
        return [
            "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/latest_leapseconds.tls",
            "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0011.tls",
            "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0012.tls",
        ]

    monkeypatch.setattr("wis.kernelspecifier.KernelSpecifier._listFD", mock_listFD)

    # Check the json file does not exist
    assert not os.path.isfile(
        KS.kernel_json
    ), f"{KS.kernel_json} should not exist at this point, but it does"

    # Call the method to generate the kernel_filepath_map
    kernel_filepath_map = KS.generate_kernel_filepath_map()

    # Assert that the kernel_filepath_map is as expected
    assert (
        len(kernel_filepath_map) == 4
    ), f"Expected 4 filepaths, but got {len(kernel_filepath_map)}"
    for f in [
        "tess2018338154429-41241_de430.bsp",
        "latest_leapseconds.tls",
        "naif0011.tls",
        "naif0012.tls",
    ]:
        assert (
            os.path.join(KS.download_subdir, f) in kernel_filepath_map
        ), f'Expected "{os.path.join(KS.download_subdir, f)}" in local_filepaths'
    assert os.path.isfile(KS.kernel_json), f"{KS.kernel_json} does not exist"


# =============================================================================
# Filepath Map Loading & Caching
# =============================================================================


def test_get_kernel_filepath_map_loads_existing(
    minimal_kernel_specifier: KernelSpecifier,
) -> None:
    """Test that get_kernel_filepath_map loads existing JSON file correctly."""
    KS = minimal_kernel_specifier

    # Write json to file using new metadata format
    input_json = {
        "/path/to/file1": {
            "remote_url": "http://example.com/file1",
            "discovery_date": "2024-01-01T00:00:00",
            "last_modified": None,
            "file_size": None,
        },
        "/path/to/file2": {
            "remote_url": "http://example.com/file2",
            "discovery_date": "2024-01-01T00:00:00",
            "last_modified": None,
            "file_size": None,
        },
    }
    with open(KS.kernel_json, "w") as f:
        json.dump(input_json, f)

    # Call the method to get the kernel_filepath_map
    kernel_filepath_map = KS.get_kernel_filepath_map()

    # Assert that the kernel_filepath_map extracts URLs correctly
    expected = {
        "/path/to/file1": "http://example.com/file1",
        "/path/to/file2": "http://example.com/file2",
    }
    assert kernel_filepath_map == expected, "kernel_filepath_map not as expected"


def test_get_kernel_metadata_loads_existing(
    minimal_kernel_specifier: KernelSpecifier,
) -> None:
    """Test that get_kernel_metadata loads existing JSON file correctly."""
    KS = minimal_kernel_specifier

    # Write json to file using new metadata format
    input_json = {
        "/path/to/file1": {
            "remote_url": "http://example.com/file1",
            "discovery_date": "2024-01-01T00:00:00",
            "last_modified": "Mon, 01 Jan 2024 00:00:00 GMT",
            "file_size": 1024,
        },
        "/path/to/file2": {
            "remote_url": "http://example.com/file2",
            "discovery_date": "2024-01-01T00:00:00",
            "last_modified": None,
            "file_size": None,
        },
    }
    with open(KS.kernel_json, "w") as f:
        json.dump(input_json, f)

    # Call the method to get the kernel metadata
    kernel_metadata = KS.get_kernel_metadata()

    # Assert that the kernel_metadata is loaded correctly
    assert kernel_metadata == input_json, "kernel_metadata not as expected"


def test_get_kernel_metadata_handles_missing_file(
    minimal_kernel_specifier: KernelSpecifier,
) -> None:
    """Test that get_kernel_metadata returns empty dict for missing file."""
    KS = minimal_kernel_specifier

    # Ensure the kernel_json file does not exist
    assert not os.path.isfile(KS.kernel_json), "kernel_json should not exist"

    # Call the method to get the kernel metadata
    kernel_metadata = KS.get_kernel_metadata()

    # Assert that an empty dict is returned
    assert (
        kernel_metadata == {}
    ), "kernel_metadata should be empty dict for missing file"


# =============================================================================
# Metadata Helper Methods
# =============================================================================


def test_format_file_size_helper(minimal_kernel_specifier: KernelSpecifier) -> None:
    """Test the _format_file_size helper method."""
    KS = minimal_kernel_specifier

    # Test various file sizes
    assert KS._format_file_size(0) == "0B"
    assert KS._format_file_size(1023) == "1023B"
    assert KS._format_file_size(1024) == "1.0KB"
    assert KS._format_file_size(1048576) == "1.0MB"
    assert KS._format_file_size(1073741824) == "1.0GB"
    assert KS._format_file_size(None) == "unknown size"


def test_calculate_file_hash_helper(
    minimal_kernel_specifier: KernelSpecifier, tmp_path: Path
) -> None:
    """Test the _calculate_file_hash helper method."""
    KS = minimal_kernel_specifier

    # Create a test file
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")

    # Calculate hash
    file_hash = KS._calculate_file_hash(str(test_file))

    # Should return a valid MD5 hash
    assert file_hash is not None
    assert len(file_hash) == 32  # MD5 hash length
    assert (
        file_hash == "9473fdd0d880a43c21b7778d34872157"
    )  # Known MD5 of "test content"


def test_is_download_older_than_helper(
    minimal_kernel_specifier: KernelSpecifier,
) -> None:
    """Test the _is_download_older_than helper method."""
    KS = minimal_kernel_specifier

    # Test with None download date
    assert KS._is_download_older_than(None)

    # Test with recent download date
    recent_date = datetime.now().isoformat()
    assert not KS._is_download_older_than(recent_date, hours=24)

    # Test with old download date
    old_date = "2024-01-01T00:00:00"
    assert KS._is_download_older_than(old_date, hours=24)

    # Test with days parameter
    assert KS._is_download_older_than(old_date, days=1)


def test_get_download_summary_helper(
    monkeypatch: pytest.MonkeyPatch, minimal_kernel_specifier: KernelSpecifier
) -> None:
    """Test the _get_download_summary helper method."""
    KS = minimal_kernel_specifier

    # Mock kernels_that_need_to_be_downloaded to return specific files
    def mock_kernels_to_download(self: KernelSpecifier) -> list[str]:
        return [
            os.path.join(self.download_subdir, "file1.bsp"),
            os.path.join(self.download_subdir, "file2.bsp"),
        ]

    monkeypatch.setattr(
        KernelSpecifier, "kernels_that_need_to_be_downloaded", mock_kernels_to_download
    )

    # Mock get_kernel_metadata to return file sizes
    def mock_get_kernel_metadata(self: KernelSpecifier) -> dict:
        return {
            os.path.join(self.download_subdir, "file1.bsp"): {"file_size": 1024},
            os.path.join(self.download_subdir, "file2.bsp"): {"file_size": 2048},
        }

    monkeypatch.setattr(
        KernelSpecifier, "get_kernel_metadata", mock_get_kernel_metadata
    )

    # Get download summary
    summary = KS._get_download_summary()

    # Assert summary contains expected data
    assert summary["file_count"] == 2
    assert summary["total_size"] == 3072  # 1024 + 2048
    assert len(summary["files_to_download"]) == 2


# =============================================================================
# Download Logic
# =============================================================================


def test_kernels_that_need_to_be_downloaded_no_staleness_checking(
    monkeypatch: pytest.MonkeyPatch, minimal_kernel_specifier: KernelSpecifier
) -> None:
    """Test that kernels_that_need_to_be_downloaded() does NOT perform staleness checking for regular files.

    This test specifically verifies the fix for the issue where staleness checking
    was being performed for all existing files, causing performance issues with
    satellite kernels that have hundreds of files.
    """
    KS = minimal_kernel_specifier

    # Add specific attributes for this test
    KS.timecritical = ["https://example.com/timecritical.bsp"]

    # Create test kernel filepath map with different scenarios:
    # - File that doesn't exist locally (should be downloaded)
    # - Regular file that exists locally (should NOT trigger staleness checking)
    # - Time-critical file that exists locally (should use time-based refresh)
    KS.kernel_filepath_map = {
        os.path.join(
            KS.download_subdir, "missing_file.bsp"
        ): "https://example.com/missing_file.bsp",
        os.path.join(
            KS.download_subdir, "regular_file.bsp"
        ): "https://example.com/regular_file.bsp",
        os.path.join(
            KS.download_subdir, "timecritical.bsp"
        ): "https://example.com/timecritical.bsp",
    }

    # Create local files for the files that should exist
    for local_path in [
        os.path.join(KS.download_subdir, "regular_file.bsp"),
        os.path.join(KS.download_subdir, "timecritical.bsp"),
    ]:
        with open(local_path, "w") as f:
            f.write("test content")

    # Create kernel metadata file with download dates
    kernel_metadata = {
        os.path.join(KS.download_subdir, "regular_file.bsp"): {
            "remote_url": "https://example.com/regular_file.bsp",
            "download_date": "2024-01-01T00:00:00",  # Old download date
            "file_size": 12,
        },
        os.path.join(KS.download_subdir, "timecritical.bsp"): {
            "remote_url": "https://example.com/timecritical.bsp",
            "download_date": "2024-01-01T00:00:00",  # Old download date (should trigger refresh)
            "file_size": 12,
        },
    }

    # Write metadata to kernel_json file
    with open(KS.kernel_json, "w") as f:
        json.dump(kernel_metadata, f)

    # Track calls to _has_remote_file_changed to ensure it's NOT called for regular files
    staleness_check_calls = []

    def mock_has_remote_file_changed(local_path: str, metadata: dict) -> bool:
        staleness_check_calls.append(local_path)
        # For this test, we'll return False (no change) but track the call
        return False

    monkeypatch.setattr(KS, "_has_remote_file_changed", mock_has_remote_file_changed)

    # Call the method under test
    files_to_download = KS.kernels_that_need_to_be_downloaded()

    # Assertions
    # 1. Missing file should be in download list
    assert os.path.join(KS.download_subdir, "missing_file.bsp") in files_to_download

    # 2. Time-critical file should be in download list (because download is old)
    assert os.path.join(KS.download_subdir, "timecritical.bsp") in files_to_download

    # 3. Regular file should NOT be in download list (no staleness checking)
    assert os.path.join(KS.download_subdir, "regular_file.bsp") not in files_to_download

    # 4. _has_remote_file_changed should NOT have been called for regular files
    #    (it should only be called for time-critical files if needed)
    regular_file_path = os.path.join(KS.download_subdir, "regular_file.bsp")
    assert (
        regular_file_path not in staleness_check_calls
    ), f"_has_remote_file_changed was called for regular file: {regular_file_path}"

    # 5. Verify the correct number of files to download
    assert (
        len(files_to_download) == 2
    ), f"Expected 2 files to download, got {len(files_to_download)}"


def test_update_kernel_metadata_helper(
    minimal_kernel_specifier: KernelSpecifier,
) -> None:
    """Test the _update_kernel_metadata helper method."""
    KS = minimal_kernel_specifier

    # Create initial kernel metadata
    initial_metadata = {
        os.path.join(KS.download_subdir, "test.bsp"): {
            "remote_url": "https://example.com/test.bsp",
            "discovery_date": "2024-01-01T00:00:00",
            "last_modified": None,
            "file_size": None,
        }
    }

    # Write initial metadata
    with open(KS.kernel_json, "w") as f:
        json.dump(initial_metadata, f)

    # Create the test file
    test_file = os.path.join(KS.download_subdir, "test.bsp")
    with open(test_file, "w") as f:
        f.write("test content")

    # Update metadata
    KS._update_kernel_metadata(test_file)

    # Load updated metadata
    with open(KS.kernel_json) as f:
        updated_metadata = json.load(f)

    # Check that metadata was updated
    file_metadata = updated_metadata[test_file]
    assert "download_date" in file_metadata
    assert "md5_hash" in file_metadata
    assert file_metadata["file_size"] == 12  # Length of "test content"
    assert file_metadata["md5_hash"] == "9473fdd0d880a43c21b7778d34872157"


def test_download_data_no_files_needed(
    minimal_kernel_specifier: KernelSpecifier, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test that download_data does nothing when no files need downloading."""
    KS = minimal_kernel_specifier

    # Mock kernels_that_need_to_be_downloaded to return empty list
    def mock_kernels_to_download(self: KernelSpecifier) -> dict:
        return {}

    monkeypatch.setattr(
        KernelSpecifier, "kernels_that_need_to_be_downloaded", mock_kernels_to_download
    )

    # Mock _get_download_summary to avoid actual file operations
    def mock_get_download_summary(self: KernelSpecifier) -> dict:
        return {"file_count": 0, "total_size": 0, "files_to_download": []}

    monkeypatch.setattr(
        KernelSpecifier, "_get_download_summary", mock_get_download_summary
    )

    # This should not raise any exceptions and should complete normally
    KS.download_data()


# =============================================================================
# Kernel Loading
# =============================================================================


def test_load_with_existing_kernels(
    monkeypatch: pytest.MonkeyPatch, minimal_kernel_specifier: KernelSpecifier
) -> None:
    """Test that the load method works with existing kernel files."""
    KS = minimal_kernel_specifier

    # MonkeyPatch the `download_data` method on `KernelSpecifier`
    def mock_download_data(self: KernelSpecifier) -> None:
        pass

    monkeypatch.setattr(
        "wis.kernelspecifier.KernelSpecifier.download_data", mock_download_data
    )

    # MonkeyPatch the `_loaded_kernels` method on `KernelSpecifier`
    def mock_loaded_kernels(self: KernelSpecifier) -> list[str]:
        return []

    monkeypatch.setattr(
        "wis.kernelspecifier.KernelSpecifier._loaded_kernels", mock_loaded_kernels
    )

    # Point the kernel_filepath_map to a file in the test_data directory
    test_file = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "test_data",
        "latest_leapseconds.tls",
    )
    KS.kernel_filepath_map = {
        test_file: "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0012.tls"
    }
    os.path.isfile(
        test_file
    )  # <- Check file exists: not part of the test, but the test won't work without it

    # Call the load method
    KS.load()

    # Test that a kernel has been loaded
    assert sp.ktotal("ALL") == 1, "No kernels loaded"


def test_loaded_kernels_helper(
    minimal_kernel_specifier: KernelSpecifier, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test the _loaded_kernels helper method."""
    KS = minimal_kernel_specifier

    # Mock spiceypy ktotal and kdata functions
    def mock_ktotal(kind: str) -> int:
        return 2

    def mock_kdata(n: int, kind: str) -> list[str]:
        return [f"kernel_{n}.bsp"]

    monkeypatch.setattr(sp, "ktotal", mock_ktotal)
    monkeypatch.setattr(sp, "kdata", mock_kdata)

    # Get loaded kernels
    loaded_kernels = KS._loaded_kernels()

    # Should return list of kernel paths
    assert loaded_kernels == ["kernel_0.bsp", "kernel_1.bsp"]


def test_load_skips_already_loaded_kernels(
    monkeypatch: pytest.MonkeyPatch, minimal_kernel_specifier: KernelSpecifier
) -> None:
    """Test that load method skips kernels that are already loaded."""
    KS = minimal_kernel_specifier

    # Mock download_data to do nothing
    def mock_download_data(self: KernelSpecifier) -> None:
        pass

    monkeypatch.setattr(KernelSpecifier, "download_data", mock_download_data)

    # Mock _loaded_kernels to return some already loaded kernels
    def mock_loaded_kernels(self: KernelSpecifier) -> list[str]:
        return [
            os.path.join(self.download_subdir, "already_loaded.bsp"),
            os.path.join(self.download_subdir, "another_loaded.bsp"),
        ]

    monkeypatch.setattr(KernelSpecifier, "_loaded_kernels", mock_loaded_kernels)

    # Set kernel_filepath_map with mixed loaded and unloaded kernels
    KS.kernel_filepath_map = {
        os.path.join(
            KS.download_subdir, "already_loaded.bsp"
        ): "https://example.com/already_loaded.bsp",
        os.path.join(
            KS.download_subdir, "another_loaded.bsp"
        ): "https://example.com/another_loaded.bsp",
        os.path.join(
            KS.download_subdir, "not_loaded.bsp"
        ): "https://example.com/not_loaded.bsp",
    }

    # Track which kernels get loaded
    loaded_kernels = []

    def mock_furnsh(kernels: list[str]) -> None:
        loaded_kernels.extend(kernels)

    monkeypatch.setattr(sp, "furnsh", mock_furnsh)

    # Call load method
    KS.load()

    # Should only load the kernel that wasn't already loaded
    assert len(loaded_kernels) == 1
    assert os.path.join(KS.download_subdir, "not_loaded.bsp") in loaded_kernels
