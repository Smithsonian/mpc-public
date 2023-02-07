"""
Test "interpret" function(s)
"""
# Third-party imports
# -----------------------
import pytest
import os

# Local imports
# -----------------------
from mpc_orb import interpret
from mpc_orb import filepaths
from mpc_orb import validate_mpcorb


# Tests
# -----------------------
def test_interpret_A(  ):
    '''
    Test that an input json filepath is correctly read ...
    '''
    
    # use the schema as an example of a valid json file
    filepath = filepaths.mpcorb_schema
    
    # read it using interpret.interpret()
    d,fp = interpret.interpret(filepath)
    
    # check the results
    assert isinstance(d, dict)
    assert fp == filepath
    
@pytest.mark.xfail
def test_interpret_B(  ):
    '''
    Test that an non-JSON file raises an exception
    '''
    
    # use the filepaths python file as an example of a NON-JSON file
    filepath = filepaths.__file__

    # read it using interpret.interpret()
    d,fp = interpret.interpret(filepath)
    

    
@pytest.mark.xfail
def test_interpret_C(  ):
    '''
    Test that an arbitrary string (that is not a file) raises an exception
    '''
    
    # string
    filepath = "bjhadfkbadkjfnkwdnflmdnf.txt"

    # read it using interpret.interpret()
    d,fp = interpret.interpret(filepath)
    

    
def test_interpret_D(  ):
    '''
    Test that an input dictionary ...
    '''
    
    # use the schema as an example of a valid json file
    filepath = filepaths.mpcorb_schema
    
    # read it using validate_mpcorb.load_json
    d_in = validate_mpcorb.load_json(filepath)
    
    # "read" d using interpret.interpret()
    d_out,fp = interpret.interpret(d_in)

    # check the results
    assert isinstance(d_out, dict)
    assert d_out == d_in
    assert fp is None
