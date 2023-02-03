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
    Test the variables defined within mpc_orb.filepaths ...
    '''
    # Test that the expected directory-related attributes exist & are directories
    for a in ["schema_dir", "fail_dir", "pass_dir"]:
        assert hasattr(filepaths,a)
        assert os.path.isdir(filepaths.__dict__[a])
        
    # Test that the expected file-related attributes exist
    for a in ["mpcorb_schema", "test_fail_mpcorb", "test_pass_mpcorb"]:
        assert hasattr(filepaths,a)

    # Test that the schema filepath is valid
    assert os.path.isfile( filepaths.mpcorb_schema ), \
        f'Error in assertion: Not a file: filepaths.mpcorb_schema={filepaths.mpcorb_schema}'
    
    # Test that the returned lists of test jsons are not empty
    for l in [ filepaths.test_fail_mpcorb , filepaths.test_pass_mpcorb ]:
        assert isinstance(l, list)
        assert len(l)
        for fp in l:
            assert os.path.isfile( fp ), f'{fp} NOT a file'

    
