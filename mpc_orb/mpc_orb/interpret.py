"""
mpc_orb/interpret.py
A convenience func to interpret an input argument as some kind of json-related input
I.e. looks to see whether its a filepath (to a json file), or a dictionary
"""

# Import third-party packages
# -----------------------
import json
from os.path import isfile


def interpret(arg):
    """
    convenience func to interpret input arg as some kind of json-related input
    I.e. looks to see whether its a filepath, a dictionary

    arg: str or dict
    
    
    returns dict
    """
    
    # try to interpret input as a json-filepath
    if isinstance(arg, str) and isfile(arg):
        try:
            with open(arg) as f:
                json_dict       = json.load(f)
                input_filepath  = arg
        except:
            raise  Exception(f"Input {arg} does not seem to be a json-file")
    
    # if its a dictionary, use that
    elif isinstance(arg, dict):
        json_dict       = arg
        input_filepath  = None
        
    # no other options yet implemented
    else:
        raise  Exception(f"Input {arg}\nis of type {type(arg)} and cannot be interpreted as json file/dict")
    
    # return the contents of the json file in dict form
    return json_dict,input_filepath

