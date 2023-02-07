"""
Defining filepaths used by mpc_orb
"""

# Import standard packages
# -----------------------
import glob
import os

# Import(s) from this package
# -----------------------
import mpc_orb.schema_json

# Directories
# -----------------------
schema_dir = mpc_orb.schema_json.__path__[0]

# Filepaths / Lists-of-Filepaths
# -----------------------
# Filepath to json schema against which everything is validated
# - Gets the highest-numbered version in the directory
mpcorb_schema = sorted( glob.glob( schema_dir + '/*.json' ) )[-1]

