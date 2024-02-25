# mpc-public/mpc_orb

Documentation and code related to the *mpc_orb.json* format. 
 - This is a standardized format for the exchange of data on the *best-fit orbit* for solar-system bodies, including minor-planets, comets, irregular satellites, and interstellar interlopers. 
 - The format uses JSON files for the exchange of data.

The MPC currently populates mpc_orb.json files using data from the *orbfit* package, but we emphasize that the 
mpc_orb.json format is intended for the generic exchange of orbit data from *any* source.  

As of May 2023, the latest version of the defining schema is version 0.4
 - While the schema versions are numbered < 1, the format should be considered experimental/developmental/beta/WIP.

This repository currently contains code and documentation related to: 
 - A description of the *mpc_orb.json* format, and an associated defining JSON schema.
 - Examples of the *mpc_orb.json* format for some specific objects
 - Python code to demonstrate the validation of files in the *mpc_orb.json* format. 
 - Python code to facilitate the parsing of files in the *mpc_orb.json* format. 

We emphasize that the *mpc_orb.json* format is intended to be language-agnostic: 
the inclusion of the python code in this repository is intended to facilitate the use of the format by the MPC and 
the wider community, but it is not intended to be the *only* way to use the format.


## Repo Contents 

 - [demos](demos) : # Example code and use cases
 - [docs](docs)	: # Documentation for both the Python package and JSON schemas	
 - [sample_json](sample_json) : Examples of the *mpc_orb.json* format for some specific objects	
 - [schema_json](schema_json) : The JSON schema files defining the *mpc_orb.json* format
 - [src](src) : Source files for Python code
 - [tests](tests) : # Test suite for the Python code



## Python Code ([src/mpc_orb](src/mpc_orb))

The [src/mpc_orb](src/mpc_orb) directory contains some python code to both validate & parse mpc-orb-json files 

More information on the code can be found in the [src/mpc_orb/README.md](src/mpc_orb/README.md) file.

N.B. The code in [src/mpc_orb](src/mpc_orb) is available as a pip-installable package:
```
pip install mpc_orb
```


## Developers 

Some information for developers can be found in the [DEVELOPERS.md](DEVELOPERS.md) file.
