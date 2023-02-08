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
from jsonschema import validate
import pkgutil


# local imports
# -----------------------
from . import interpret
from . import filepaths


# IO function(s)
# -----------------------
#def load_json( json_filepath ):
#    """ Load a json file into a dictionary
#    """
#    with open( json_filepath ) as f:
#        return json.load(f)
        
def load_schema( ):
    """ Use pkgutil to load schema into a dictionary
    """
    # use pkgutil to get resource ...
    raw_bytes = pkgutil.get_data(__name__ , filepaths.schema_relative_filepath)
    return json.loads(raw_bytes.decode('utf-8'))




# Validation function(s)
# -----------------------
def validate_mpcorb( arg ):
    """
    Test whether the supplied json is a valid example of an mpcorb json
    Input can be json-filepath, or dictionary of json contents
    
    arg: dictionary or json-filepath
     - The input json to be validated`
    
    returns: Boolean
    
    """

    # interpret the input (allow dict or json-filepath)
    data, input_filepath = interpret.interpret(arg)

    # validate
    # NB # If no exception is raised by validate(), the instance is valid.
    validate(   instance = data,  schema = load_schema( ))
    
    return True

