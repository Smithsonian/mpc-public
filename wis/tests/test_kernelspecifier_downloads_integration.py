"""Integration Tests for the KernelSpecifier class.

 - These tests should be run RARELY as they require internet access,
   and it's rude to hammer on other people's servers.

*** NB Only data downloads that require internet access are tested here
*** See test_kernels.py for the rest of the standard unit-tests

"""

# Third-party imports
# -----------------------------------------
import os
from pathlib import Path

import pytest

# Local imports
# -----------------------------------------
from wis.kernelspecifier import KernelSpecifier

pytestmark = pytest.mark.integration

# Test Functions
# -----------------------------------------


# ------- KernelDownloader ----------------


def test_KernelSpecifier__listFD(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Test that the _listFD() method works as expected.

    NB:
    As-of 2025-01-25,
    https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/
    contains ...
    [PARENTDIR] Parent Directory                                -
    [DIR] a_old_versions/            2016-07-14 17:00    -
    [TXT] aareadme.txt               2018-05-29 16:44  792
    [TXT] latest_leapseconds.tls     2016-07-14 17:00  5.1K
    [TXT] latest_leapseconds.tls.pc  2016-07-14 17:02  5.3K
    [TXT] naif0011.tls               2016-08-22 22:36  5.0K
    [TXT] naif0012.tls               2016-07-14 17:00  5.1K
    [TXT] naif0012.tls.pc            2016-07-14 17:02  5.3K
    """
    # Create a properly initialized KernelSpecifier instance
    monkeypatch.setattr("wis.constants.Directories.data_dir", tmp_path)
    KS = KernelSpecifier(
        obscodeMPC="000",
        obscodeJPL="000",
        name="Test Observatory",
        files=["https://example.com/test.tls"],
        wildcards={},
    )

    # Define the URL and wildcard
    url, wildcard = "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/", "*.tls"

    # Call the method
    result = KS._listFD(url, wildcard=wildcard)

    # Check that the method has at least returned naif0011.tls  & naif0012.tls
    # Obviously this test is subject to the website being moved/removed/updated/reorganized/...
    for f in [
        "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/latest_leapseconds.tls",
        "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0011.tls",
        "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0012.tls",
    ]:
        assert f in result, f'Expected "{f}" in result'


def test_KernelSpecifier_download_data(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Test that direct file download works (using 'download_data()' ).

    N.B. This also tests underlying 'kernels_have_been_downloaded()'.

    NB:
    As-of 2025-01-25,
    https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/
    contains ...
    [PARENTDIR] Parent Directory                                -
    [DIR] a_old_versions/            2016-07-14 17:00    -
    [TXT] aareadme.txt               2018-05-29 16:44  792
    [TXT] latest_leapseconds.tls     2016-07-14 17:00  5.1K
    [TXT] latest_leapseconds.tls.pc  2016-07-14 17:02  5.3K
    [TXT] naif0011.tls               2016-08-22 22:36  5.0K
    [TXT] naif0012.tls               2016-07-14 17:00  5.1K
    [TXT] naif0012.tls.pc            2016-07-14 17:02  5.3K
    """
    # Create a properly initialized KernelSpecifier instance
    monkeypatch.setattr("wis.constants.Directories.data_dir", tmp_path)
    KS = KernelSpecifier(
        obscodeMPC="000",
        obscodeJPL="000",
        name="Test Observatory",
        files=["https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/aareadme.txt"],
        wildcards={"https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/": "*.tls"},
        timecritical=[],
    )

    # Call the method
    KS.download_data()
    # Check that the files have been downloaded
    # Files are downloaded to download_subdir, not tmp_path directly
    for f in ["aareadme.txt", "latest_leapseconds.tls", "naif0011.tls", "naif0012.tls"]:
        assert os.path.isfile(
            os.path.join(KS.download_subdir, f)
        ), f'Expected "{f}" in download directory {KS.download_subdir}'
