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
    Test the variables defined within mpc_orb.filepaths ...
    '''
  
    # Test that the expected attributes exist
    for a in ["pack_dir", "json_dir", "mpcorb_schema", "test_fail_mpcorb", "test_pass_mpcorb"]:
        assert hasattr(filepaths,a)

    # Test that the schema filepath is valid
    assert os.path.isfile( filepaths.mpcorb_schema ), \
        f'Error in assertion: Not a file: filepaths.mpcorb_schema={filepaths.mpcorb_schema}'
    
    # Test that the returned lists of test jsons are not empty
    for l in [ filepaths.test_fail_mpcorb , filepaths.test_pass_mpcorb ]:
        assert isinstance(l, list)
        assert len(l)
        for fp in l:
            assert os.path.isfile( fp )
    
    
