"""
Test validation schema
"""

# Standard imports
# -----------------------
import json
import os
import pytest

# Local imports
# -----------------------
from mpc_orb.filepaths import MPCORB_FILEPATHS as FILEPATHS
from mpc_orb import validate_mpcorb

def load_package_json(filepath_relative_to_package):
    ''' get json & return as dict '''
    with open( os.path.join(FILEPATHS().code_dir,filepath_relative_to_package) ) as user_file:
        return json.load( user_file )


def test_schema():
    ''' Test that the *load_schema* function works ... '''
    assert validate_mpcorb.load_schema(), \
        f'could not open schema'

def test_validation_A():
    ''' Test that valid json-file(s) successfully validate '''
    F = FILEPATHS()
    assert F.valid_sample_relative_filepaths, f'F.valid_sample_relative_filepaths: {F.valid_sample_relative_filepaths}'
    for fp in F.valid_sample_relative_filepaths:
        data_dict = load_package_json( os.path.join(FILEPATHS().code_dir,fp) )

        assert validate_mpcorb.validate_mpcorb( data_dict ), \
            f'could not validate data_dict from {os.path.join(FILEPATHS().code_dir,fp) }'

def test_validation_B(  ):
    '''
    Test that all invalid JSON-files in the 'test_fail_mpcorb' directory FAIL validation as expected
    '''
    F = FILEPATHS()
    assert F.invalid_sample_relative_filepaths
    for fp in F.invalid_sample_relative_filepaths:
        data_dict = load_package_json( os.path.join(FILEPATHS().code_dir,fp) )

        assert not validate_mpcorb.validate_mpcorb( data_dict ), 'Expected **IN**valid'

@pytest.mark.xfail
def test_validation_C(  ):
    '''
    Test that all invalid JSON-files in the 'test_fail_mpcorb' directory FAIL validation as expected
     - Here we are testing whether an exception is raised when we set *raise_exception_if_invalid* to True
    '''
    F = FILEPATHS()
    assert F.invalid_sample_relative_filepaths
    for fp in F.invalid_sample_relative_filepaths:
        data_dict = load_package_json( os.path.join(FILEPATHS().code_dir,fp) )

        assert not validate_mpcorb.validate_mpcorb( data_dict , raise_exception_if_invalid=True )
