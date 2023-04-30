"""
Defining filepaths used by mpc_orb
"""

# Import standard packages
# -----------------------
import os

# Directories / Filepaths / ...
# -----------------------
# The directory of this script
code_dir = os.path.dirname(os.path.realpath(__file__))

# Relative filepath to json schema against which everything is validated
# - Gets the highest-numbered version in the directory
schema_relative_filepath = "schema_json/mpcorb_schema_latest.json"

# Relative path to directory containing sample mpc_orb JSON files
# - Expected to be used to facilitate various demonstrations
demo_dir = "demo_json/"

# Filepath(s) for sample mpc_orb JSON files
demo_2012HN13 = os.path.join(code_dir, demo_dir, "2012HN13_mpcorb_yarkovski.json")
