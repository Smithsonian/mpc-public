"""
Defining filepaths used by mpc_orb
"""

# Import standard packages
# -----------------------
import glob



# Filepaths / Lists-of-Filepaths
# -----------------------
# Filepaths to sample json files used in tests
test_fail_mpcorb = glob.glob( "test_jsons/fail_mpcorb/*.json" )
test_pass_mpcorb = glob.glob( "test_jsons/pass_mpcorb/*.json" )



