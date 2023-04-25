# mpc-public/mpc_orb


Code related to the "mpc_orb.json" format.

This format is intended to be used to describe the orbits of solar-system minor-planets, comets, irregular satellites, and interstellar interlopers.

The MPC currently populates mpc_orb.json files using data from the orbfit package, but we emphasize that the mpc_orb.json format is intended for the generic exchange of orbit data from any source.  

As of April 2023, the latest version of the defining schema is version 0.4
 - While the schema versions are numbered < 1, the format should be considered experimental/developmental/beta/WIP.

The repo currently contains code and documentation related to: 
 - A description of the "mpc_orb.json" format, and an associated defining JSON schema.
 - Python code to demonstrate the validation of files in the "mpc_orb.json" format. 
 - Python code to facilitate the parsing of files in the "mpc_orb.json" format. 

## Repo Contents 

(a) demos            

 - Demonstrations of python code usage, including *python-scripts* and *jupyter notebooks*.


(b) mpc_orb            

 - The main python code directory.

 - Contains code to both validate & parse mpc-orb-json files 
 
 - Contains directories holding the defining schema (*/mpc_orb/schema_json/*) and sample files (*/mpc_orb/demo_json/*). 

(c) docs 

 - Documentation describing the "mpc_orb.json" format, including *allowed* fields, *required* fields, etc

(d) tests

 - Tests of the python code in the *mpc_orb* directory. For details of the test code, including how to execute the tests, please see the file */tests/README.md*.


## MPC_ORB JSON schema 

 - The JSON files defining the "mpc_orb.json" format can be found in */mpc_orb/schema_json*
 
 - Further documentation on the format can be found in */docs/*




## Python Functionalities (*mpc_orb*)

(i) Provide "parse" functions for JSON files containing "MPC_ORB.JSON" formatted data

 - It is expected that this functionality will be used regularly by both internal MPC staff & external community users.

 - The parsing code is in mpc_orb/parse.py

 - Demonstrations of code usage can be found in demo/Example_parse_mpcorb_json.ipynb and demo/demo_parse.py


(ii) Provide validation functions

 - It is expected that these validation functionalities will typically be used as part of the "parse" functions described in (i) above. 
 
 - I.e. it is *not* expected that the end-user will directly access the validation functions themselves, but rather, the validation functions are called under-the-hood by the mpc_orb/parse.py routines. 

 - The code that performs the validation can be found in mpc_orb/validate_mpcorb.py


## Installation and Usage 

The python code in *mpc_orb* is available as a pip-installable python package. 

To do so the user can type:
> pip install mpc_orb

 

