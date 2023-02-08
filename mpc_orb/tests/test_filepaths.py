"""
Test parsing class/functions
"""
# Third-party imports
# -----------------------
import pytest
import os

# Local imports
# -----------------------
from mpc_orb import filepaths


# Tests
# -----------------------
def test_filepaths_A(  ):
    '''
    Test the variable(s) defined within mpc_orb.filepaths ...
    '''
    # Test that the expected attributes exist
    for a in ["schema_relative_filepath"]:
        assert hasattr(filepaths,a)
        
    
