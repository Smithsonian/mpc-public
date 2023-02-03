"""
Defining filepaths used by mpc_orb
"""

# Import third-party packages
# -----------------------
import glob
from os.path import join, dirname, abspath
import os

import mpc_orb.json_files.schema_json
import mpc_orb.json_files.test_jsons.fail_mpcorb
import mpc_orb.json_files.test_jsons.pass_mpcorb

# Directories
# -----------------------
schema_dir = mpc_orb.json_files.schema_json.__path__[0]
fail_dir   = mpc_orb.json_files.test_jsons.fail_mpcorb.__path__[0]
pass_dir   = mpc_orb.json_files.test_jsons.pass_mpcorb.__path__[0]


# Filepaths / Lists-of-Filepaths
# -----------------------
# Filepath to json schema against which everything is validated
mpcorb_schema = os.path.join(schema_dir, 'mpcorb_schema.json')

# Filepaths to sample json files used in tests
test_fail_mpcorb = glob.glob( fail_dir + "/*.json" )
test_pass_mpcorb = glob.glob( pass_dir + "/*.json" )



