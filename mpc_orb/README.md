# mpc-public/mpc_orb

N.B. The code in this repository is available as a pip-installable package:
```
pip install mpc_orb
```

Documentation and code related to the *mpc_orb.json* format. 
 - This is a standardized format for the exchange of data on the *best-fit orbit* for solar-system bodies, including minor-planets, comets, irregular satellites, and interstellar interlopers. 
 - The format uses JSON files for the exchange of data.

The MPC currently populates mpc_orb.json files using data from the *orbfit* package, but we emphasize that the mpc_orb.json format is intended for the generic exchange of orbit data from *any* source.  

As of May 2023, the latest version of the defining schema is version 0.4
 - While the schema versions are numbered < 1, the format should be considered experimental/developmental/beta/WIP.

This repository currently contains code and documentation related to: 
 - A description of the *mpc_orb.json* format, and an associated defining JSON schema.
 - Examples of the *mpc_orb.json* format for some specific objects
 - Python code to demonstrate the validation of files in the *mpc_orb.json* format. 
 - Python code to facilitate the parsing of files in the *mpc_orb.json* format. 

## Repo Contents 


### Sample JSON Files 

Examples of the *mpc_orb.json* format for some specific objects can be found in */mpc_orb/demo_json*
 

### MPC_ORB JSON schema 

The JSON files defining the *mpc_orb.json* format can be found in */mpc_orb/schema_json*
 
### Documentation

Documentation describing the *mpc_orb.json* format, including *allowed* fields, *required* fields, constraints, etc, can be found in the */docs/* directory.


### Python Functionalities (*/mpc_orb/*)

The */mpc_orb/* directory contains some python code to both validate & parse mpc-orb-json files 

#### Parsing *mpc_orb.json* formatted data

The code in *mpc_orb/parse.py* provides functions & classes to facilitate the parsing of *mpc_orb.json* files in python. 

It is expected that this functionality will be used regularly by both internal MPC staff & external community users.

Some demonstrations of code usage can be found in the */demo/* directory and in the *mpc_orb/demo.py* script.


#### Validating *mpc_orb.json* files

The code in *mpc_orb/parse.py* provides functions & classes to validate *mpc_orb.json* files in python. 

It is expected that these validation functionalities will typically be used as part of the "parse" functions described above. 

I.e. it is *not* expected that the end-user will regularly access the validation functions *directly*, but rather, the validation functions will be called under-the-hood by the *mpc_orb/parse.py* routines. 



#### Installation and Usage 

The python code in *mpc_orb* is available as a pip-installable python package. 

```
pip install mpc_orb
```
 


### Python Tests (*/tests/*)

Tests of the python code in the *mpc_orb* directory are provided in the *tests* directory. 
 
 For details of the test code, including how to execute the tests, please see the file */tests/README.md*.


