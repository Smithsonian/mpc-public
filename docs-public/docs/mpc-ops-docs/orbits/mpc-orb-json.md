# MPC_ORB JSON Format

The MPC_ORB JSON format provides a JSON representation of orbital elements and related parameters for standard epoch orbits. It represents the Minor Planet Center's effort to establish a standardized format for exchanging orbital data across different institutions and software packages.


## Python Package

The MPC maintains the [mpc_orb](https://github.com/Smithsonian/mpc-public/tree/main/mpc_orb) package in the [mpc-public](https://github.com/Smithsonian/mpc-public) repository. It can be installed via [pip](https://pypi.org/project/mpc-orb/):

```bash
pip install mpc_orb
```

The package provides:

- Format descriptions
- Multiple format examples
- Python code for schema validation
- Python parsing utilities


## Schema

The complete schema is available in [mpcorb_schema_latest.json](https://github.com/Smithsonian/mpc-public/blob/main/mpc_orb/mpc_orb/schema_json/mpcorb_schema_latest.json).

!!! note
    While the schema version is still `0.x`, the schema is subject to change.


## Accessing MPC_ORB Data

MPC_ORB JSON is available as an output option when querying the [Orbits API](../apis/get-orb.md).


## Feedback

Community feedback is welcomed through the [MPC helpdesk](https://mpc-service.atlassian.net/servicedesk/customer/portals).
