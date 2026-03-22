# mpc_client

Python client for the [Minor Planet Center](https://minorplanetcenter.net/) APIs.

`mpc_client` wraps every MPC public REST API into a single `MPCClient` class
with input validation, structured error handling, and optional pandas DataFrame
output.

## Installation

```bash
pip install mpc-client              # core (returns dicts)
pip install mpc-client[dataframe]   # adds pandas DataFrame methods
```

## Quick Start

```python
from mpc_client import MPCClient

mpc = MPCClient()

# Identify an object
info = mpc.identify("Ceres")

# Get orbital elements
orbit = mpc.get_orbit("Bennu")

# Get observations as a DataFrame
df = mpc.get_observations_df("Bennu")
```

## API Coverage

| API | Methods |
|-----|---------|
| Designation Identifier | `identify()` |
| Observatory Codes | `get_observatory()`, `get_all_observatories()`, `search_observatories()` |
| Observations | `get_observations()`, `get_observations_df()` |
| NEOCP Observations | `get_neocp_observations()`, `get_neocp_observations_df()` |
| Orbits | `get_orbit()`, `get_orbit_raw()` |
| MPECs | `get_mpecs()`, `get_discovery_mpec()` |
| Check Near-Duplicates | `check_near_duplicates()`, `count_near_duplicates()` |
| Submission Status | `get_submission_status()` |
| Action Codes | `request_action_code()` |
| Submission | `submit_xml()`, `submit_psv()` |

## Contact

- **Bug reports & feature requests:** [GitHub Issues](https://github.com/Smithsonian/mpc-public/issues)
- **General MPC enquiries:** [MPC Jira Helpdesk](https://mpc-service.atlassian.net/servicedesk/customer/portals)

## License

`mpc_client` is released under the [MIT License](https://github.com/Smithsonian/mpc-public/blob/main/LICENSE).

## Acknowledgments

Developed by the **Minor Planet Center** at the
[Smithsonian Astrophysical Observatory](https://www.cfa.harvard.edu/sao),
under funding provided by NASA's Planetary Defense Coordination Office.
