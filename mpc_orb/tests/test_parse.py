"""
Test parsing class/functions
"""
# Third-party imports
# -----------------------
import pytest
from os.path import join, dirname, abspath

# Local imports
# -----------------------
from mpc_orb import MPCORB, COORD
from mpc_orb import filepaths


# Tests
# -----------------------

def test_MPCORB_A(  ):
    '''
    Test the parsing of mpcorb-jsons ...
    Instantiate empty
    '''
  
    M = MPCORB()
    assert isinstance(M,MPCORB)

def test_MPCORB_B(  ):
    '''
    Test the parsing of mpcorb-jsons ...
    Instantiate with file
    '''
  
    # Loop over the mpcorb files that are expect to "pass"
    # Attempt to instantiate using each ...
    for f in filepaths.test_pass_mpcorb:
        M = MPCORB(f)
        
        assert isinstance(M,MPCORB)


def test_parse_C(  ):
    '''
    Test the parsing of mpcorb-jsons ...
    Check basic attributes
    '''
  
    # Loop over the mpcorb files that are expect to "pass"
    # Attempt to instantiate using each ...
    for f in filepaths.test_pass_mpcorb:
        M = MPCORB(f)
        for k in ['COM','CAR','categorization', 'epoch_data', 'designation_data', 'magnitude_data', 'non_grav_booleans', 'orbit_fit_statistics', 'software_data', 'system_data']:
            assert hasattr(M,k)
            
def test_parse_D(  ):
    '''
    Test the CAR & COM sub-classes ...
    Check element attributes
    '''
    for f in filepaths.test_pass_mpcorb:
        M = MPCORB(f)

        for I,expected_names  in zip(   [M.COM, M.CAR], \
                                        [["q","e","i","node","argperi","peri_time"], ["x","y","z","vx","vy","vz"] ]):

            # Check that we have a "COORD" object
            assert isinstance(I, COORD)

            # Check that "I" has the expected "bulk" attributes ...
            for key in ['coefficient_names', 'coefficient_values', 'coefficient_uncertainties', 'eigenvalues', 'covariance', 'covariance_array', 'element_dict']:
                assert hasattr(I, key)

            # Check that "I" has the expected individual attributes ...
            for name in expected_names:
                assert hasattr(I, name)
                assert isinstance( I.__dict__[name], dict) and "val" in I.__dict__[name] and "unc" in I.__dict__[name]

            # Check that the individual attribute values are the same as the element_dict entries
            # E.g. I.element_dict["x"] == I.x
            for name in expected_names:
                assert I.element_dict[name] == I.__dict__[name]


        # Double-check that the individual attributes (e.g. "x" or "e") are accessible directly from the MPCORB object, M
        for name in ["q","e","i","node","argperi","peri_time"] + ["x","y","z","vx","vy","vz"] :
            assert hasattr(M, name)
        

def test_describe_A(  ):
    '''
    Test the describe function
    '''

    for f in filepaths.test_pass_mpcorb[:1]:
        M = MPCORB(f)

        for key in [ _ for _ in M.__dict__.keys() if _ != 'schema_json']:
            description_dict = M.describe(key)
            assert isinstance(description_dict, dict)
            assert key in description_dict
            assert isinstance(description_dict[key], dict), f'-----------------------------------{key}'
            assert description_dict[key] is not None
