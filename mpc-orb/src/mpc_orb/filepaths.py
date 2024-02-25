"""
Defining filepaths used by mpc_orb
"""

# Import standard packages
# -----------------------
import os
import glob

# Directories / Filepaths / ...
# -----------------------
class MPCORB_FILEPATHS():
    """
    Class to hold filepaths used by mpc_orb
    """
    def __init__(self, ):

        # The directory of this script
        self.code_dir = os.path.dirname(os.path.abspath(__file__))

        # Relative filepath to json schema against which everything is validated
        self.schema_relative_filepath = "schema_json/mpcorb_schema_latest.json"

        # Relative path to directory containing sample mpc_orb JSON files
        # - Expected to be used for testing & demos
        self.valid_sample_dir = "sample_json/valid/"
        self.invalid_sample_dir = "sample_json/invalid/"

        # Filepath(s) for samples of *VALID* & *INVALID* mpc_orb JSON files
        self.valid_sample_relative_filepaths = self._get_sample_json_filepaths(self.valid_sample_dir)
        self.invalid_sample_relative_filepaths = self._get_sample_json_filepaths(self.invalid_sample_dir)


    def _get_sample_json_filepaths(self, sample_dir):
        """
        Method to create list of JSONs in the sample directory
        """
        # Create list of JSONs in the sample directory
        return [ os.path.join(sample_dir, os.path.basename(f)) for f in glob.glob(os.path.join(self.code_dir , sample_dir) + "/*.json")]
