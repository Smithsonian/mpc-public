# mpc-public/mpc_orb


Code related to the parsing & validation of best-fit orbit files in the "mpc_orb.json" format.

This format is intended to be used to describe the orbits of solar-system minor-planets, comets, irregular satellites, and interstellar interlopers.

The MPC currently populates mpc_orb.json files using data from the orbfit package, but we emphasize that the mpc_orb.json format is intended for the generic exchange of orbit data from any source.  

## Functionalities 

(i) Provide "parse" functions for JSON files containing "MPC_ORB.JSON" formatted data

 - It is expected that this functionality will be used regularly by both internal MPC staff & external community users.

 - The parsing code is in mpc_orb/parse.py

 - Demonstrations of code usage can be found in demo/Example_parse_mpcorb_json.ipynb and demo/demo_parse.py


(ii) Provide validation functions

 - It is expected that these validation functionalities will typically be used as part of the "parse" functions described in (i) above. 
 - I.e. it is *not* expected that the end-user will directly access the validation functions themselves, but rather, the validation functions are called under-the-hood by the mpc_orb/parse.py routines. 

 - The code that performs the validation can be found in mpc_orb/validate_mpcorb.py


## Installation and Usage 

It is intended that this become a pip-installable python package. 

Once that has been set-up, "pip install mpc_orb" instructions should be placed here.  
 
## Repo Contents 

(a) demos            

 - Demonstrations of code usage.

 - Both python-scripts and jupyter notebooks.


(b) mpc_orb            

 - The main code directory.

 - Contains code to both validate & parse mpc-orb-json files 


(c) mpc_orb/json_files

 - Sample JSON files.

 - Both the defining validation schema and some sample jsons for testing.


(d) tests

 - Tests of the code in mpc_orb
 
