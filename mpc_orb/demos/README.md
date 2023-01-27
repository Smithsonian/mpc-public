# Demonstrations & Examples

Code to illustrate the usage of various components of the mpc_orb package

### (1) How to read/parse a given mpc_orb.json file

 - It is expected that these parsing functions will be used regularly by both internal MPC staff & external community users.

 - The code to do the parsing is provided in mpc_orb/parse.py

 - Both "demo_parse.py" and "Example_parse_mpcorb_json.ipynb" provide the same basic example of how to parse a given mpc_orb.json file using the code in the mpc_orb/parse.py module. 

### (2) Docker stuff

 - Dockerfile, build_container.py & pythonServer.py work to allow creation of a bare-bones container with the mpc_orb package in it. 
 
 - If you have docker installed & working, then executing "python3 build_container.py" should ...
    - Build an image that contains the mpc_orb code, and has all of the requirements installed
    - Deploy the container

