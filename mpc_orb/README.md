# `mpc_orb`

`mpc_orb` is a Python package and reference repository for working with
`mpc_orb.json` orbit files.

The format is designed to exchange best-fit orbit information for a single
solar-system object, including orbital elements, covariance information,
fit statistics, metadata, and optional non-gravitational terms.

The package can:

- validate an `mpc_orb.json` payload against the bundled JSON schema
- parse a JSON file or Python dictionary into a convenient Python object
- expose orbit content in a form that is easier to inspect and use in code

## Installation

Install from PyPI:

```bash
pip install mpc_orb
```

Install from this repository while developing:

```bash
pip install -e .
```

Install with test dependencies:

```bash
pip install -e .'[test]'
```

## Quick Start

```python
from mpc_orb.parse import MPCORB
from mpc_orb import validate_mpcorb
import json

json_path = "tests/jsons/pass_mpcorb/2012HN13_mpcorb_yarkovsky.json"

# Read json into a dictionary
with open(json_path, "r", encoding="utf-8") as f:
    json_dict = json.load(f)

# Optional explicit validation
validate_mpcorb.validate_mpcorb(json_dict)

# Parse into a Python object
M = MPCORB(json_dict)

# Top-level metadata
print(M.designation_data["iau_name"])
print(M.software_data["mpcorb_version"])

# Cometary elements
print(M.COM.q["val"], M.COM.q["unc"])
print(M.COM.e["val"], M.COM.e["unc"])

# Cartesian elements
print(M.CAR.x["val"], M.CAR.x["unc"])
print(M.CAR.vx["val"], M.CAR.vx["unc"])

# Convenience aliases
print(M.q["val"])
print(M.x["val"])

# Full covariance matrix
print(M.CAR.covariance_array.shape)

# Optional Keplerian elements
if hasattr(M, "KEP"):
    print(M.KEP.a["val"])
```

## Main API

### `MPCORB`

The main entry point is `mpc_orb.parse.MPCORB`.

```python
from mpc_orb.parse import MPCORB

M = MPCORB(json_dict)
```

When you instantiate `MPCORB`, the package:

1. interprets the input as either a JSON filepath or a Python dictionary
2. validates the content against the packaged schema
3. exposes the parsed content as object attributes

You can also instantiate an empty object and parse later:

```python
from mpc_orb.parse import MPCORB

M = MPCORB()
M.parse(json_dict)
```

### `validate_mpcorb`

Validation helpers live in `mpc_orb.validate_mpcorb`.

```python
from mpc_orb import validate_mpcorb

validate_mpcorb.validate_mpcorb(json_dict)
```

If the input is valid, the function returns `True`. If it is not valid, it
raises an exception from the validation layer.

### `describe`

`MPCORB.describe()` uses the schema to describe a field and, when available,
report its units.

```python
info = M.describe("q")
print(info)
```

## Parsed Data Model

An `MPCORB` instance exposes both raw JSON sections and convenience structures
created during parsing.

### Top-Level Attributes

These sections are attached directly to the `MPCORB` instance as dictionaries:

- `categorization`
- `designation_data`
- `epoch_data`
- `magnitude_data`
- `moid_data`
- `non_grav_booleans`
- `orbit_fit_statistics`
- `software_data`
- `system_data`

### Coordinate Containers

`COM`, `CAR`, and optional `KEP` (starting from version 0.6) are represented as `COORD` objects. 
Each one includes:

- `coefficient_names`
- `coefficient_values`
- `coefficient_uncertainties`
- `eigenvalues`
- `covariance`
- `covariance_array`
- `element_dict`

Individual fitted quantities are also exposed as attributes such as:

- `M.COM.q`
- `M.CAR.x`
- `M.KEP.a`

Each of these is a dictionary with `val` and `unc` keys.

## Accepted Inputs

Most public functions in the package accept a Python `dict` containing the JSON content.

That behavior is implemented in `mpc_orb/interpret.py` and is shared by the
parser and validator.

## Schema And Version Handling

The versioned schema files live in `mpc_orb/schema_json/`.

Validation is version-aware: `validate_mpcorb.validate_mpcorb()` reads
`software_data["mpcorb_version"]` from the input JSON and loads the matching
schema file bundled with the package.

If you call `load_schema()` directly with no version, the package loads the
`latest` schema alias:

```python
from mpc_orb import validate_mpcorb

schema = validate_mpcorb.load_schema()
```

## Repository Contents

- `mpc_orb/`: Python package code
- `mpc_orb/schema_json/`: versioned JSON schema files
- `mpc_orb/demo_json/`: sample `mpc_orb.json` files
- `demos/`: notebook-based usage examples
- `docs/`: format documentation and generated PDFs
- `tests/`: parser and validation tests

## Examples And Demo Material

The repository includes a few ready-made examples:

- `mpc_orb/demo_json/` contains sample JSON files
- `mpc_orb/bin/demo.py` provides a simple command-line demo
- `demos/Example_parse_mpcorb_json.ipynb` shows interactive usage

After installation, the demo entry point is also exposed as:

```bash
demo
```

## Running The Tests

From the `mpc_orb` project directory:

```bash
pytest -v tests
```

The test suite covers:

- schema loading and validation behavior
- parsing of `COM`, `CAR`, and optional `KEP` sections
- convenience attributes such as `M.q` and `M.x`
- schema-backed descriptions returned by `describe()`

## Notes

The MPC currently generates `mpc_orb.json` files from `orbfit`, but the format
is intended for broader orbit-data exchange and is not tied to a single orbit
determination pipeline.

## Documentation
Documentation for `mpc_orb` is available on the [MPC Public Documentation Hub](https://docs.minorplanetcenter.net/), and tutorials for working with `mpc_orb.json` files are available on the [MPC Orbit API tutorial page](https://docs.minorplanetcenter.net/tutorials/notebooks/mpc_tutorial_api_orbits/).
