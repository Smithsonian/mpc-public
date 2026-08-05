"""Tests for instantiated examples of KernelSpecifier objects for SATELLITES.

NB: This is *NOT* testing the wis.Satellite object: see test_wis_Satellite.py for that.
"""

# -----------------------------------------
# Local imports
# -----------------------------------------
from wis.kernel_instances_satellites import (
    GAIA,
    HST,
    JWST,
    KEPLER,
    TESS,
    satellite_kernels,
)
from wis.kernelspecifier import KernelSpecifier

# -----------------------------------------
# Test Functions
# -----------------------------------------


def test_kernel_spec_satellites_a() -> None:
    """Test the contents of the satellite_kernels dict from kernel_spec_satellites.py."""
    # Test that all expected satellites are present in the satellite_kernels dict
    # Test that only expected satellites are present in the satellite_kernels dict
    expected_satellites = ["C55", "C57", "258", "250", "274"]
    for k in expected_satellites:
        assert (
            k in satellite_kernels
        ), f"KernelSpecifier for {k} not found in satellite_kernels"
    for k in satellite_kernels:
        assert (
            k in expected_satellites
        ), f"Unexpected KernelSpecifier for {k} found in satellite_kernels"

    # Test that all entries in the dict are KernelSpecifier objects
    for _k, v in satellite_kernels.items():
        assert isinstance(v, KernelSpecifier)


def test_individual_kernel_exports() -> None:
    """Test that satellite kernels are exported as individual KernelSpecifier objects."""
    # Test Kepler
    assert isinstance(KEPLER, KernelSpecifier), "KEPLER should be a KernelSpecifier"
    assert KEPLER.obscodeMPC == "C55", "KEPLER obscodeMPC should be C55"
    assert KEPLER.obscodeJPL == "-227", "KEPLER obscodeJPL should be -227"
    assert KEPLER.name == "Kepler/K2", "KEPLER name should be Kepler/K2"

    # Test TESS
    assert isinstance(TESS, KernelSpecifier), "TESS should be a KernelSpecifier"
    assert TESS.obscodeMPC == "C57", "TESS obscodeMPC should be C57"
    assert TESS.obscodeJPL == "-95", "TESS obscodeJPL should be -95"
    assert TESS.name == "TESS", "TESS name should be TESS"

    # Test GAIA
    assert isinstance(GAIA, KernelSpecifier), "GAIA should be a KernelSpecifier"
    assert GAIA.obscodeMPC == "258", "GAIA obscodeMPC should be 258"
    assert GAIA.obscodeJPL == "-123", "GAIA obscodeJPL should be -123"
    assert GAIA.name == "Gaia", "GAIA name should be Gaia"

    # Test HST
    assert isinstance(HST, KernelSpecifier), "HST should be a KernelSpecifier"
    assert HST.obscodeMPC == "250", "HST obscodeMPC should be 250"
    assert HST.obscodeJPL == "-48", "HST obscodeJPL should be -48"
    assert HST.name == "HST", "HST name should be HST"

    # Test JWST
    assert isinstance(JWST, KernelSpecifier), "JWST should be a KernelSpecifier"
    assert JWST.obscodeMPC == "274", "JWST obscodeMPC should be 274"
    assert JWST.obscodeJPL == "-170", "JWST obscodeJPL should be -170"
    assert JWST.name == "JWST", "JWST name should be JWST"


def test_kernel_attributes() -> None:
    """Test that exported kernels have required attributes."""
    for kernel in [KEPLER, TESS, GAIA, HST, JWST]:
        # Check required attributes exist
        assert hasattr(kernel, "obscodeMPC")
        assert hasattr(kernel, "obscodeJPL")
        assert hasattr(kernel, "name")
        assert hasattr(kernel, "files")
        assert hasattr(kernel, "wildcards")
        assert hasattr(kernel, "timecritical")

        # Check attribute types
        assert isinstance(kernel.obscodeMPC, str)
        assert isinstance(kernel.obscodeJPL, str)
        assert isinstance(kernel.name, str)
        assert isinstance(kernel.files, list)
        assert isinstance(kernel.wildcards, dict)
        assert isinstance(kernel.timecritical, list)
