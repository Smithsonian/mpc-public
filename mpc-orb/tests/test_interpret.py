"""
Test "interpret" function(s)
"""
# Third-party imports
# -----------------------
import pytest
import os

# Local imports
# -----------------------
from mpc_orb.filepaths import MPCORB_FILEPATHS as FILEPATHS
from mpc_orb import interpret

# Tests
# -----------------------

def test_interpret_A(  ):
    '''
    Test that an input json filepath is correctly read ...
    '''
    
    # use the schema as an example of a valid json file
    F = FILEPATHS()
    schema_filepath = os.path.join(F.code_dir,F.schema_relative_filepath)

    # read it using interpret.interpret()
    d, fp = interpret.interpret(schema_filepath)

    # check the results
    assert isinstance(d, dict)
    assert fp == schema_filepath



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
    
    # string (this is NOT a file that exists)
    filepath = "bjhadfkbadkjfnkwdnflmdnf.txt"

    # read it using interpret.interpret()
    d,fp = interpret.interpret(filepath)
    

    
def test_interpret_D(  ):
    '''
    Test that an input dictionary is correctly interpreted ...
    '''
    
    # An arbitrary dictionary
    d_in = {"a":1, "b":2, "c":3}
    
    # "read" d using interpret.interpret()
    d_out,fp = interpret.interpret(d_in)

    # check the results
    assert isinstance(d_out, dict)
    assert d_out == d_in
    assert fp is None
