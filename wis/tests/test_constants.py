"""Test the physical constants and directories defined in wis.constants."""

import os
import shutil

from wis.constants import AllowedDEs, Directories, PhysicalConstants


def test_AllowedDEs() -> None:
    """Test that the allowed emphemeris enum is as expected."""
    for s in ["DE430", "DE440"]:
        assert s in AllowedDEs, f"{s} not in AllowedDEs"
    for s in ["foo", "bar"]:
        assert s not in AllowedDEs, f"{s} in AllowedDEs"


def test_PhysicalConstants() -> None:
    """Test that the PhysicalConstants dataclass is as expected."""
    assert (
        PhysicalConstants.Rearth_km == 6378.1363
    ), f"Rearth_km not as expected: {PhysicalConstants.Rearth_km}"
    assert (
        PhysicalConstants.au_km == 149597870.700
    ), f"au_km not as expected: {PhysicalConstants.au_km}"
    assert (
        PhysicalConstants.Rearth_AU
        == PhysicalConstants.Rearth_km / PhysicalConstants.au_km
    ), f"Rearth_AU not as expected: {PhysicalConstants.Rearth_AU}"
    assert (
        PhysicalConstants.day_s == 86400
    ), f"day_s not as expected: {PhysicalConstants.day_s}"


def test_Directories() -> None:
    """Test that the Directories class is as expected."""
    D = Directories()
    assert D.data_dir == os.path.join(
        os.path.expanduser("~"), ".wispykernels"
    ), f"data_dir not as expected: {D.data_dir}"
    assert D.obscode_data_subdir("test") == os.path.join(
        D.data_dir, "test"
    ), f'obscode_data_subdir not as expected: {D.obscode_data_subdir("test")}'
    assert os.path.exists(D.data_dir), f"data_dir does not exist: {D.data_dir}"
    assert os.path.exists(
        D.obscode_data_subdir("test")
    ), f'obscode_data_subdir does not exist: {D.obscode_data_subdir("test")}'
    assert os.path.isdir(D.data_dir), f"data_dir is not a directory: {D.data_dir}"
    assert os.path.isdir(
        D.obscode_data_subdir("test")
    ), f'obscode_data_subdir is not a directory: {D.obscode_data_subdir("test")}'

    # Clean up
    shutil.rmtree(D.obscode_data_subdir("test"))
