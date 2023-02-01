"""
Test validation schema
"""



# Standard imports
# -----------------------
import pytest
import os
import sys

# Local imports
# -----------------------
from mpc_orb import validate_mpcorb
from mpc_orb import filepaths


# High level tests
# -----------------------


"""
names_of_variables     = ('dictionary_key_for_filepaths')
values_for_each_test   = [
    # We expect the jsons in the 'test_pass_mpcorb' directory to pass ...
    ('test_pass_mpcorb'),
    # We expect the jsons in the 'test_fail_mpcorb' directory to fail ...
    pytest.param('test_fail_mpcorb',
                 marks=pytest.mark.xfail(reason='Expected fail, invalid file'))
]
@pytest.mark.parametrize( names_of_variables , values_for_each_test )
def test_validation_mpcorb_A( dictionary_key_for_filepaths ):
    '''
    Test the validation of MPCORB jsons (numerical jsons)
    Here we test that
    (1) all of the JSONs in the 'test_pass_mpcorb' directory pass validation as expected
    (2) all of the JSONs in the 'test_fail_mpcorb' directory fail validation as expected
    '''
  
    # The filepath_dict from filepaths contains the locations of a number of test files
    for f in filepath_dict[dictionary_key_for_filepaths]:
        schema.validate_mpcorb(f)
"""

# Lower level tests
# -----------------------

def test_schema():
    ''' Test that the supplied schema is a valid (loadable) json'''
    assert validate_mpcorb.load_json( filepaths.mpcorb_schema ), f'could not open {filepaths.mpcorb_schema}'

def test_pass_file():
    ''' Test that a single, valid json-file successfully loads'''
    assert os.path.isfile(filepaths.test_pass_mpcorb[0])
    assert validate_mpcorb.load_json( filepaths.test_pass_mpcorb[0] ), f'could not open {filepaths.test_pass_mpcorb[0]}'

def test_validation():
    ''' Test that a single, valid json-file successfully validates'''
    assert validate_mpcorb.validate_mpcorb( filepaths.test_pass_mpcorb[0] ), f'could not validate {filepaths.test_pass_mpcorb[0]}'
