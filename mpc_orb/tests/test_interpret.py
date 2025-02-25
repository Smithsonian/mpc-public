"""
Test "interpret" function(s)
"""

# Third-party imports
# -----------------------
import pytest
from pathlib import Path

# Local imports
# -----------------------
from mpc_orb import interpret
from mpc_orb import validate_mpcorb

JSON_DIR = Path(__file__).parent / "jsons"


@pytest.mark.parametrize(
    "valid_json_files",
    [
        [f"{JSON_DIR}/pass_mpcorb/2012HN13_mpcorb_yarkovsky.json"],
    ],
)
def test_interpret_valid_json_files(valid_json_files):
    """
    Test that an input json filepath is correctly read
    """

    # Loop over the mpcorb files that are expect to "pass"
    for k in valid_json_files:
        full_path = k
        # read it using interpret.interpret()
        d = interpret.interpret(full_path)

        # check the results
        assert isinstance(d, dict)


@pytest.mark.parametrize(
    "invalid_json_files",
    [
        [f"{JSON_DIR}/fail_mpcorb/2012HN13_mpcorb.json"],
    ],
)
@pytest.mark.xfail
def test_interpret_invalid_json_files(invalid_json_files):
    """
    Test that an non-JSON file raises an exception
    """

    # Loop over the mpcorb files that are expect to "fail"
    for k in invalid_json_files:
        full_path = k
        # read it using interpret.interpret()
        d = interpret.interpret(full_path)

        assert isinstance(d, dict)


@pytest.mark.xfail
def test_interpret_arbitrary_string():
    """
    Test that an arbitrary string (that is not a file) raises an exception
    """

    # string (this is NOT a file that exists)
    filepath = "bjhadfkbadkjfnkwdnflmdnf.txt"

    # read it using interpret.interpret()
    d = interpret.interpret(filepath)


def test_interpret_input_dictionary():
    """
    Test that an input dictionary is correctly interpreted ...
    """

    # use the schema as an example of a valid json file
    # read it using validate_mpcorb.load_json
    d_in = validate_mpcorb.load_schema()

    # "read" d using interpret.interpret()
    d_out = interpret.interpret(d_in)

    # check the results
    assert isinstance(d_out, dict)
    assert d_out == d_in
