"""
Defining filepaths used by mpc_orb
"""

# Import third-party packages
# -----------------------
import glob
from os.path import join, dirname, abspath
import os

# Directories
# -----------------------
pack_dir  = '/Users/matthewjohnpayne/Envs/mpc-public/mpc_orb/mpc_orb/'      # Directory for code
json_dir  = os.path.join(pack_dir, 'json_files')  # Directory for supplied JSON files


# Filepaths / Lists-of-Filepaths
# -----------------------
# Filepath to json schema against which everything is validated
mpcorb_schema = os.path.join(json_dir, 'schema_json', 'mpcorb_schema.json')

# Filepaths to sample json files used in tests
test_fail_mpcorb = glob.glob( os.path.join(json_dir, 'test_jsons', 'fail_mpcorb' + "/*" ) )
test_pass_mpcorb = glob.glob( os.path.join(json_dir, 'test_jsons', 'pass_mpcorb' + "/*" ) )



