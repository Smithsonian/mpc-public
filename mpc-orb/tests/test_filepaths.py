"""
Test parsing class/functions
"""
# Standard imports
# -----------------------
import os
# Local imports
# -----------------------
from mpc_orb.filepaths import MPCORB_FILEPATHS as FILEPATHS


# Tests
# -----------------------
def test_filepaths_A(  ):
    '''
    Test instantiation ...
    '''
    # Test instantiation ...
    F = FILEPATHS()
    assert isinstance(F, FILEPATHS  )

def test_filepaths_B():
    '''
    Test the variable(s) defined within mpc_orb.filepaths ...
    '''
    F = FILEPATHS()

    # Test that the expected attributes exist
    for a in ["code_dir", "schema_relative_filepath", "valid_sample_dir", "invalid_sample_dir",
              "valid_sample_relative_filepaths", "invalid_sample_relative_filepaths"]:
        assert hasattr(F, a)

    # Test the expected files/directories exist
    assert os.path.isdir(F.code_dir)

    for d in [F.valid_sample_dir, F.invalid_sample_dir]:
        assert os.path.isdir(os.path.join(F.code_dir,d)), f'd={d}, but os.path.isdir(d)={os.path.isdir(d)}'

    assert os.path.isfile(os.path.join(F.code_dir,F.schema_relative_filepath)), f'Not a file ... f={f}'

    for f in F.valid_sample_relative_filepaths + F.invalid_sample_relative_filepaths:
        assert os.path.isfile(os.path.join(F.code_dir,f)), f'Not a file ... f={f}'

def test_filepaths_C():
    '''
    Test specific sample-files exist (because we will use it/them in demos)
    '''
    F = FILEPATHS()
    assert os.path.isfile( os.path.join(F.code_dir,F.valid_sample_dir,'2012HN13_mpcorb_yarkovski.json'))
