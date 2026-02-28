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

### Testing / Reviewing 

The `.github` workflow should release a new version of `mpc_api` to `TestPyPI` every time 
a PR is opened or updated. 
If reviews would like to test the latest version of `mpc_api` from TestPyPI, you can run:
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ mpc-api                                                                                                                
```
where `--index-url` points to TestPyPI for mpc-api itself, while `--extra-index-url` falls back to real PyPI for its 
dependencies (requests, pandas, etc.) which aren't on TestPyPI.       


### Release 

A `.github` workflow will release a new version of `mpc_api` to `PyPI` 
every time a PR that touches `mpc_api` is merged into `main`, 
**as long as the version is updated in `pyproject.toml`**.


### To-Do

There are a number of MPC APIs that are not yet implemented in `mpc_api`. 
These include (but are not limited to):
 - Pointings Submission
 - Pointings Retrieval
 - Submission of Identifications
 - NEO Rating == digest2: https://minorplanetcenter.net/iau/NEO/PossNEO.html
 - ...

Each of these APIs should:
1. Have documentation and a tutorial notebook added to the [MPC docs website](https://docs.minorplanetcenter.net/) 
2. Have a corresponding method added to `mpc_api` that is tested and documented.
