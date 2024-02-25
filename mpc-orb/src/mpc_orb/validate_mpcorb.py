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
from jsonschema import validate, exceptions
import pkgutil


# local imports
# -----------------------
from . import interpret
from .filepaths import MPCORB_FILEPATHS as FILEPATHS


# IO function(s)
# -----------------------
        
def load_schema( ):
    """ Use pkgutil to load schema into a dictionary
    """

    # use pkgutil to get resource ...
    raw_bytes = pkgutil.get_data(__name__ , FILEPATHS().schema_relative_filepath)
    return json.loads(raw_bytes.decode('utf-8'))




# Validation function(s)
# -----------------------
def validate_mpcorb( arg , raise_exception_if_invalid = False):
    """
    Test whether the supplied json is a valid example of an mpcorb json
    Input can be json-filepath, or dictionary of json contents
    
    arg: dictionary or json-filepath
     - The input json to be validated`

    raise_exception_if_invalid: Boolean
     - If True, an exception is raised if the input is invalid
     - If False, the function returns False if the input is invalid
    
    returns: Boolean

    """

    # interpret the input (allow dict or json-filepath)
    data, input_filepath = interpret.interpret(arg)

    # validate
    #  - raise exception or return True/False as appropriate
    # NB # If no exception is raised by validate(), the instance is valid.
    try:
        validate(   instance = data,  schema = load_schema( ))
        return True
    except Exception as excep:
        if raise_exception_if_invalid:
            raise ValueError(excep)
        else:
            return False

