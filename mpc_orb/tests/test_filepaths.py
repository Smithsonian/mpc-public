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
def test_filepaths_B(  ):
    '''
    Test the variable(s) defined within mpc_orb.filepaths ...
    '''
    # Test that the expected directory-related attributes exist & are directories
    for a in ["schema_dir"]:
        assert hasattr(filepaths,a)
        assert os.path.isdir(filepaths.__dict__[a])
        
    # Test that the expected file-related attributes exist
    for a in ["mpcorb_schema"]:
        assert hasattr(filepaths,a)

    # Test that the schema filepath is valid
    assert os.path.isfile( filepaths.mpcorb_schema ), \
        f'Error in assertion: Not a file: filepaths.mpcorb_schema={filepaths.mpcorb_schema}'
    
    
