"""
Test validation schema
"""

# Standard imports
# -----------------------
import json
from pathlib import Path
import pytest


# Local imports
# -----------------------
from mpc_orb import validate_mpcorb

JSON_DIR = Path(__file__).parent / "jsons"


def test_schema():
    """Test that the *load_schema* function works ..."""
    assert validate_mpcorb.load_schema(), "could not open schema"

@pytest.mark.parametrize(
    "valid_json_files",
    [
        [f"{JSON_DIR}/pass_mpcorb/2012HN13_mpcorb_yarkovsky.json"],
    ],
)
def test_validation_json_files(valid_json_files):
    """Test that valid json-files successfully validate"""
    for k in valid_json_files:
        with open(k, "r", encoding="utf-8") as f:
            data_dict = json.load(f)
        assert validate_mpcorb.validate_mpcorb(
            data_dict
        ), f"could not validate data_dict from {k}"


@pytest.mark.parametrize(
    "invalid_json_files",
    [
        [f"{JSON_DIR}/fail_mpcorb/2012HN13_mpcorb.json"],
    ],
)
def test_validation_single_json_fail(invalid_json_files):
    """Test that invalid json-files fail validation"""
    for k in invalid_json_files:
        with open(k, "r", encoding="utf-8") as f:
            data_dict = json.load(f)
        with pytest.raises(Exception):
            validate_mpcorb.validate_mpcorb(data_dict)

