Set of tools that analyze digest2 output and distinguishes NEOs from non-NEOs.

The analysis is described in Cloete, R. and Veres, P.: Near-Earth Object Discovery Enhancement with the Machine Learning Methods

Data:

neocp.obs - obs80 (MPC1992) format of NEOPC data between 2019 - 2024. The designations were altered: last 6 characters are from trkid, first character is either '0' (NEO) or '1' (non-NEO).
digest_data_19-24.csv - digest2 values for 2019 - 2023 NEOCP data
digest_data_24.csv - digest2 values for 2024 NEOCP data
MPC.config - configuration file for digest2
optimal_thresholds.json - derived filter threshold (limit = 0)

Tools:

find_filter.py - takes digest2 output (e.g. digest_data_19-24.csv) in a csv format, creates JSON threshold model "optimal_thresholds.json" for the following tool
example usage: python3 find_filter.py digest_data_19-24.csv

neocp_filter.py - selects assumed non-NEOs from the input file (digest2 output, e.g. digest_data_24.csv) based on the JSON model
example usage: neocp_filter.py digest_data_24.csv optimal_thresholds.json

