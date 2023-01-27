"""
Test validation schema
"""
# Third-party imports
# -----------------------
import pytest

# Local imports
# -----------------------
from os.path import join, dirname, abspath

import sys
pack_dir  = dirname(dirname(abspath(__file__))) # Package directory
code_dir  = join(pack_dir, 'mpc_orb')           # Code directory
sys.path.append(code_dir)

import schema
from filepaths import filepath_dict


# High level tests
# -----------------------

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


# Lower level tests
#(***NOT YET IMPLEMENTED*** )
# -----------------------

