"""Tests for instantiated examples of KernelSpecifier objects for GROUND based observatories."""

# -----------------------------------------
# Local imports
# -----------------------------------------
from wis.constants import AllowedDEs
from wis.kernel_instances_ground import DE430, DE440, GROUND
from wis.kernelspecifier import KernelSpecifier

# -----------------------------------------
# Test Functions
# -----------------------------------------


def test_kernel_spec_ground_a() -> None:
    """Test the contents of the GROUND dict from kernel_instances_ground.py."""
    # Test that GROUND is a dict
    assert isinstance(GROUND, dict)

    # Check that the keys are as expected
    assert sorted(GROUND.keys()) == sorted([_.value for _ in AllowedDEs])

    # Check that the values are KernelSpecifier objects
    for value in GROUND.values():
        assert isinstance(value, KernelSpecifier)


def test_individual_kernel_exports() -> None:
    """Test that DE430 and DE440 are exported as individual KernelSpecifier objects."""
    # Test DE430
    assert isinstance(DE430, KernelSpecifier), "DE430 should be a KernelSpecifier"
    assert DE430.obscodeMPC == "GROUND430", "DE430 obscodeMPC should be GROUND430"
    assert DE430.name == "DE430", "DE430 name should be DE430"
    assert "de430.bsp" in str(DE430.files), "DE430 should include de430.bsp file"

    # Test DE440
    assert isinstance(DE440, KernelSpecifier), "DE440 should be a KernelSpecifier"
    assert DE440.obscodeMPC == "GROUND440", "DE440 obscodeMPC should be GROUND440"
    assert DE440.name == "DE440", "DE440 name should be DE440"
    assert "de440.bsp" in str(DE440.files), "DE440 should include de440.bsp file"


def test_kernel_attributes() -> None:
    """Test that exported kernels have required attributes."""
    for kernel in [DE430, DE440]:
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

        # Check files contain expected kernel files
        files_str = str(kernel.files)
        assert (
            "latest_leapseconds.tls" in files_str
        ), "Should include leap seconds kernel"
        assert "pck" in files_str, "Should include planetary constants kernel"


def test_consistency_with_ground_dict() -> None:
    """Test that individual exports are consistent with GROUND dict."""
    assert (
        GROUND["DE430"] is DE430
    ), "GROUND['DE430'] should be the same object as DE430"
    assert (
        GROUND["DE440"] is DE440
    ), "GROUND['DE440'] should be the same object as DE440"
