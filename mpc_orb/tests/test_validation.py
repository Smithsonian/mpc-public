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
    print("***"*33)
    print(f'***load_package_json***: __package__={__package__} , filepath_relative_to_package = {filepath_relative_to_package}')
    raw_bytes = pkgutil.get_data(__package__ , filepath_relative_to_package)
    return json.loads(raw_bytes.decode('utf-8'))
    

# Lower level tests
# -----------------------
def test_schema():
    ''' Test that the supplied schema is a valid (loadable) json'''
    assert validate_mpcorb.load_schema(), \
        f'could not open schema'

"""
def test_pass_file():
    ''' Test that a single, valid json-file successfully loads'''
    assert os.path.isfile(filepaths_for_testing.test_pass_mpcorb[0])
    #assert validate_mpcorb.load_json( filepaths_for_testing.test_pass_mpcorb[0] ), \
    #    f'could not open {filepaths_for_testing.test_pass_mpcorb[0]}'

"""

def test_validation_A():
    ''' Test that a single, valid json-file successfully validates'''
    data_dict = load_package_json(filepaths_for_testing.test_pass_yarkovski)
    assert validate_mpcorb.validate_mpcorb( data_dict ), \
        f'could not validate data_dict from {filepaths_for_testing.test_pass_yarkovski}'

"""

# High level tests
# -----------------------
def test_validation_B(  ):
    '''
    Test that all valid JSON-files in the 'test_pass_mpcorb' directory pass validation as expected
    '''
  
    # The filepath_dict from filepaths contains the locations of a number of test files
    for f in filepaths_for_testing.test_pass_mpcorb:
        validate_mpcorb.validate_mpcorb(f)


@pytest.mark.xfail
def test_validation_C(  ):
    '''
    Test that all invalid JSON-files in the 'test_fail_mpcorb' directory FAIL validation as expected
    '''
    for f in filepaths_for_testing.test_fail_mpcorb:
        validate_mpcorb.validate_mpcorb(f)
"""
