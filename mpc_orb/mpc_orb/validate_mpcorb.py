"""
mpc_orb/validate.py
 - Code to *validate* a candidate json-file against a schema file
 - Expected to primarily be used VIA THE MPCORB class in parse.py

Author(s)
MJP
"""

# Standdard imports
# -----------------------
import json
from pathlib import Path
from jsonschema import validate


# local imports
# -----------------------
from mpc_orb import interpret


def load_schema(version=None):
    """ Load schema file """
    # If not version, then latest is assumed
    if version is None:
        version = "latest"
        
    schema_dir = Path(__file__).parent / "schema_json"
    schema_file = schema_dir / f"mpcorb_schema_v{version}.json"

    with open(schema_file, "r", encoding="utf-8") as f:
        schema = json.load(f)
        
    return schema 

# Validation function(s)
# -----------------------
def validate_mpcorb(arg):
    """
    Test whether the supplied json is a valid example of an mpcorb json
    Input can be json-filepath, or dictionary of json contents

    arg: dictionary or json-filepath
     - The input json to be validated`

    returns: Boolean

    """

    # interpret the input (allow dict or json-filepath)
    data = interpret.interpret(arg)

    # read the version
    version = data["software_data"]["mpcorb_version"]
    if version is None:
        raise ValueError("No version number found in the input json")

    schema = load_schema(version)

    # validate
    # NB # If no exception is raised by validate(), the instance is valid.
    validate(instance=data, schema=schema)

    return True
