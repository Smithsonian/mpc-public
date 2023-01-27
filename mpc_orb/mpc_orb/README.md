# mpc_orb/mpc_orb

The main code directory for the mpc_orb package

As of 2023-01 most/all of this code can be blamed on MJP

## Contains the following main components

### Python Code

(1) filepaths.py
 - Simple file to define the directory structure & filepaths of this package

(2) interpret.py
 - Convenience func to interpret an input arg as some kind of JSON-related input
 - Entirely possible that the json-package can already do this

(3) parse.py
 - Code to parse an mpc_orb JSON file
 - Expected to be used frequently to read the contents of an mpc_orb.json
 - Expected to be of use to the external community as well as to the MPC
 - Some simple demos of this code can be found in "demos/Example_parse_mpcorb_json.ipynb" and "demos/demo_parse.py"

(4) validate_mpcorb.py
 - Code to *validate* a candidate json-file against the mpc_orb schema file


### JSON Directory

(a) json_files
 - Directory to store various JSON files.
 - Includes both schema-JSONs & test-/demo-JSONs 
