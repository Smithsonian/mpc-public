# mpc_client

Python client for the [Minor Planet Center](https://minorplanetcenter.net/) APIs.

`mpc_client` wraps every MPC public REST API into a single `MPCClient` class
with typed response models, input validation, structured error handling, and
optional pandas DataFrame output.

## Installation

```bash
pip install mpc-client              # core (returns typed objects)
pip install mpc-client[dataframe]   # adds pandas DataFrame methods
```

## Quick Start

```python
from mpc_client import MPCClient

mpc = MPCClient()

# Identify an object
info = mpc.identify("Ceres")

# Get orbital elements (returns OrbitalElements object)
orbit = mpc.get_orbit("Bennu")
print(orbit.designation_data.permid)

# Get observations as a DataFrame
df = mpc.get_observations_df("Bennu")
```

## API Coverage

| API | Methods | Returns |
|-----|---------|---------|
| Designation Identifier | `identify()` | `Dict[str, DesignationInfo]` |
| Observatory Codes | `get_observatory()`, `get_all_observatories()`, `search_observatories()` | `Observatory` |
| Observations | `get_observations()`, `get_observations_df()` | `ObservationsResult` / DataFrame |
| NEOCP Observations | `get_neocp_observations()`, `get_neocp_observations_df()` | `ObservationsResult` / DataFrame |
| Orbits | `get_orbit()`, `get_orbit_raw()` | `OrbitalElements` |
| MPECs | `get_mpecs()`, `get_discovery_mpec()` | `MPEC` |
| Check Near-Duplicates | `check_near_duplicates()`, `count_near_duplicates()` | `Dict[str, List[NearDuplicateMatch]]` |
| Submission Status | `get_submission_status()` | `SubmissionStatus` |
| Action Codes | `request_action_code()` | `ActionCodeResponse` |
| Submission | `submit_xml()`, `submit_psv()` | `SubmissionResponse` |

## Contact

- **Bug reports & feature requests:** [GitHub Issues](https://github.com/Smithsonian/mpc-public/issues)
- **General MPC enquiries:** [MPC Jira Helpdesk](https://mpc-service.atlassian.net/servicedesk/customer/portals)

## License

`mpc_client` is released under the [MIT License](https://github.com/Smithsonian/mpc-public/blob/main/LICENSE).

## Acknowledgments

Developed by the **Minor Planet Center** at the
[Smithsonian Astrophysical Observatory](https://www.cfa.harvard.edu/sao),
under funding provided by NASA's Planetary Defense Coordination Office.
