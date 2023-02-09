"""
Test validation schema
"""



# Standard imports
# -----------------------
import pytest
import os
import sys
import pkgutil
import json

# Local imports
# -----------------------
from mpc_orb import validate_mpcorb
from mpc_orb import filepaths
from . import filepaths_for_testing


def load_package_json(filepath_relative_to_package):
    ''' use pkgutil to get resource & return as dict '''
    raw_bytes = pkgutil.get_data(__package__ , filepath_relative_to_package)
    return json.loads(raw_bytes.decode('utf-8'))
    

# Lower level tests
# -----------------------
def test_schema():
    ''' Test that the supplied schema is a valid (loadable) json'''
    assert validate_mpcorb.load_schema(), \
        f'could not open schema'

def test_validation_A():
    ''' Test that a single, valid json-file successfully validates'''
    data_dict = load_package_json(filepaths_for_testing.test_pass_yarkovski)
    assert validate_mpcorb.validate_mpcorb( data_dict ), \
        f'could not validate data_dict from {filepaths_for_testing.test_pass_yarkovski}'



# High level tests
# -----------------------
def test_validation_B(  ):
    '''
    Test that all valid JSON-files in the 'test_pass_mpcorb' directory pass validation as expected
    '''
  
    # Get all of the json filenames defined in filepaths_for_testing that have '...pass...' in the name
    # NB : At the time of writing there was only one filepath ... in which case test_validation_B == test_validation_A
    valid_jsons = [k for k in filepaths_for_testing.__dict__ if "__" not in k and "pass" in k]
    assert valid_jsons
    for k in valid_jsons:
        data_dict = load_package_json(filepaths_for_testing.__dict__[k])
        assert validate_mpcorb.validate_mpcorb( data_dict )



@pytest.mark.xfail
def test_validation_C(  ):
    '''
    Test that all invalid JSON-files in the 'test_fail_mpcorb' directory FAIL validation as expected
    '''
    invalid_jsons = [k for k in filepaths_for_testing.__dict__ if "__" not in k and "fail" in k]
    assert invalid_jsons
    for k in invalid_jsons:
        data_dict = load_package_json(filepaths_for_testing.__dict__[k])
        assert validate_mpcorb.validate_mpcorb( data_dict )

