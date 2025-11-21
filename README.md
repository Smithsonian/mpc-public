# mpc-public

An over-arching repository to hold various publicly-released pieces of code written by the MPC

Notes for MPC staff/developers can be found in *DEVELOPER_NOTES.md*

## Current contents 

As of May 2023, only the *mpc_orb* component exists within *mpc-public*.
The MPC intends to add additional components over the coming months. 

### mpc_orb
Last Update: 2025-02-25
 - Introduction of a new version: 0.5
 - Documentation and code related to a standardized format for the exchange of data on the *best-fit orbit* for solar-system bodies. 
 - The format uses JSON files for the exchange of data, and is refered to as the *mpc_orb.json* format.
 - Documentation is also available on the (https://minorplanetcenter.net/mpcops/documentation/mpc-orb-json/)[MPC Documentation page]
 - The *mpc_orb* repository includes:
    - json-schema files to define the standard;
    - sample orbit files in the format;
    - python code to parse & validate example orbit files.

### digest2
Last Update: 2025-11-21
 - XML-enhanled repository of digest2 code, population model and the configuration files.
