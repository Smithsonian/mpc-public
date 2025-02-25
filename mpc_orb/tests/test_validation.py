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


def test_validation_single_json():
    """Test that a single, valid json-file successfully validates"""
    with open(
        f"{JSON_DIR}/pass_mpcorb/2012HN13_mpcorb_yarkovsky.json", "r", encoding="utf-8"
    ) as f:
        data_dict = json.load(f)
    assert validate_mpcorb.validate_mpcorb(
        data_dict
    ), f"could not validate data_dict from {JSON_DIR}/pass_mpcorb/2012HN13_mpcorb_yarkovsky.json"


def test_validation_single_json_fail():
    """Test that a single, invalid json-file fails validation"""
    with open(
        f"{JSON_DIR}/fail_mpcorb/2012HN13_mpcorb.json", "r", encoding="utf-8"
    ) as f:
        data_dict = json.load(f)
    with pytest.raises(Exception):
        validate_mpcorb.validate_mpcorb(data_dict)
