# mpc_orb/mpc_orb

The main code directory for the mpc_orb package

N.B. The code in this repository is available as a pip-installable package:
```
pip install mpc_orb
```

## Package Components

### Python Code

(0) demo.py
 - A basic demonstration script that can be called immediately after installation. 
 - Provides some simple examples of how to use *parse.py* (see below), while simultaneously demonstrating that installation has actually worked.

(1) filepaths.py
 - Convenience module to define the directory structure & filepaths of this package

(2) interpret.py
 - Convenience module to interpret an input arg as some kind of JSON-related input
 - Entirely possible that the json-package can already do this, and that this module is redundant. 

(3) parse.py
 - Code to parse an mpc_orb JSON file
 - Expected to be used frequently to read the contents of an mpc_orb.json
 - Expected to be of use to the external community as well as to the MPC
 - Some simple demos of this code can be found in *demos/Example_parse_mpcorb_json.ipynb*, *demos/demo_parse.py*, and *demos.py*

(4) validate_mpcorb.py
 - Code to *validate* a candidate json-file against the mpc_orb schema file


### *schema_json* Directory

 - Directory to store schema-JSONs 
 - These are used define the acceptable fields (and values) for mpc_orb.json files


### *demo_json* Directory

- Directory to store sample JSON file(s) to illustrate example(s) of the *mpc_orb.json* format 
