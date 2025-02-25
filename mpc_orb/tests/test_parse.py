"""
Test parsing class/functions
"""

# Standard imports
# -----------------------
import pkgutil
import json
from pathlib import Path
import pytest

# Local imports
# -----------------------
from mpc_orb.parse import MPCORB, COORD

JSON_DIR = Path(__file__).parent / "jsons"

def load_json(json_file):
    """Read the file and return the json as a dictionary"""
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)


def test_instantiate_mpcorb():
    """
    Test the parsing of mpcorb-jsons ...
    Instantiate empty
    """

    M = MPCORB()
    assert isinstance(M, MPCORB)

@pytest.mark.parametrize(
    "valid_json_files",
    [
        [f"{JSON_DIR}/pass_mpcorb/2012HN13_mpcorb_yarkovsky.json"],
    ],
)
def test_parsing_mpcorb(valid_json_files):
    """
    Test the parsing of mpcorb-jsons 
    Instantiate with file
    """

    for k in valid_json_files:
        data_dict = load_json(k)
        M = MPCORB(data_dict)
        assert isinstance(M, MPCORB)


@pytest.mark.parametrize(
    "valid_json_files",
    [
        [f"{JSON_DIR}/pass_mpcorb/2012HN13_mpcorb_yarkovsky.json"],
    ],
)
def test_parse_mpcorb_basic_attributes(valid_json_files):
    """
    Test the parsing of mpcorb-jsons 
    Check basic attributes
    """

    for k in valid_json_files:
        data_dict = load_json(k)
        M = MPCORB(data_dict)

        for k in [
            "COM",
            "CAR",
            "categorization",
            "epoch_data",
            "designation_data",
            "magnitude_data",
            "non_grav_booleans",
            "orbit_fit_statistics",
            "software_data",
            "system_data",
        ]:
            assert hasattr(M, k)

@pytest.mark.parametrize(
    "valid_json_files",
    [
        [f"{JSON_DIR}/pass_mpcorb/2012HN13_mpcorb_yarkovsky.json"],
    ],
)
def test_parse_car_com(valid_json_files):
    """
    Test the CAR & COM sub-classes 
    Check element attributes
    """

    for k in valid_json_files:
        data_dict = load_json(k)
        M = MPCORB(data_dict)

        for I, expected_names in zip(
            [M.COM, M.CAR],
            [
                ["q", "e", "i", "node", "argperi", "peri_time"],
                ["x", "y", "z", "vx", "vy", "vz"],
            ],
        ):

            # Check that we have a "COORD" object
            assert isinstance(I, COORD)

            # Check that "I" has the expected "bulk" attributes ...
            for key in [
                "coefficient_names",
                "coefficient_values",
                "coefficient_uncertainties",
                "eigenvalues",
                "covariance",
                "covariance_array",
                "element_dict",
            ]:
                assert hasattr(I, key)

            # Check that "I" has the expected individual attributes ...
            for name in expected_names:
                assert hasattr(I, name)
                assert (
                    isinstance(I.__dict__[name], dict)
                    and "val" in I.__dict__[name]
                    and "unc" in I.__dict__[name]
                )

            # Check that the individual attribute values are the same as the element_dict entries
            # E.g. I.element_dict["x"] == I.x
            for name in expected_names:
                assert I.element_dict[name] == I.__dict__[name]

        # Double-check that the individual attributes (e.g. "x" or "e") are accessible directly from the MPCORB object, M
        for name in ["q", "e", "i", "node", "argperi", "peri_time"] + [
            "x",
            "y",
            "z",
            "vx",
            "vy",
            "vz",
        ]:
            assert hasattr(M, name)


@pytest.mark.parametrize(
    "valid_json_files",
    [
        [f"{JSON_DIR}/pass_mpcorb/2012HN13_mpcorb_yarkovsky.json"],
    ],
)
def test_describe_function(valid_json_files):
    """
    Test the describe function
    """

    for k in valid_json_files:
        data_dict = load_json(k)
        version = data_dict["software_data"]["mpcorb_version"]
        M = MPCORB(data_dict)

        for key in [_ for _ in M.__dict__ if _ != "schema_json"]:
            description_dict = M.describe(key, version)
            print(description_dict)
            assert isinstance(description_dict, dict)
            assert key in description_dict
            assert isinstance(
                description_dict[key], dict
            ), f"-----------------------------------{key}"
            assert description_dict[key] is not None
