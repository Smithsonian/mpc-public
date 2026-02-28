# mpc_api

Python client for the [Minor Planet Center](https://minorplanetcenter.net/) APIs.

## Installation

```bash
pip install mpc-api
```

For DataFrame support:

```bash
pip install mpc-api[dataframe]
```

## Quick Start

```python
from mpc_api import MPCClient

mpc = MPCClient()

# Identify an object
info = mpc.identify("Ceres")

# Get orbital elements
orbit = mpc.get_orbit("Bennu")

# Get observations as a DataFrame
df = mpc.get_observations_df("Bennu")

# Check for near-duplicate observations
dupes = mpc.check_near_duplicates(
    "     K10CM6D  C2023 05 16.43686615 56 36.807-23 12 43.67         21.55wX     F51"
)
```
## Tutorial Notebook

A jupyter notebook tutorial covering the basics of using `mpc_api` is available
[here](https://docs.minorplanetcenter.net/tutorials/notebooks/mpc_tutorial_mpcapi/
).

## API Coverage

| API | Method |
|-----|--------|
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

## Documentation

- [API Tutorials](https://docs.minorplanetcenter.net/tutorials/api_tutorials/)
- [MPC Operations Documentation](https://minorplanetcenter.net/mpcops/documentation/)

## Development

```bash
cd mpc_api
pip install -e '.[test]'
pytest -v
```
