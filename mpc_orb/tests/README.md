# `mpc_orb`

`mpc_orb` is a small Python package for reading, validating, and inspecting
`mpc_orb.json` orbit files.

The format is intended for exchanging best-fit orbit information for a single
solar-system object, including orbital elements, covariance information,
fit statistics, metadata, and optional non-gravitational terms.

## What The Package Does

The package is built around three core tasks:

- Validate an `mpc_orb.json` payload against one of the bundled schema files.
- Parse a JSON file or Python dictionary into a convenient `MPCORB` object.
- Expose orbit content in a way that is easier to work with from Python.

In practice, this means you can point the package at a file on disk or pass it
an already-loaded dictionary, and then access fields such as:

- top-level metadata like `designation_data`, `epoch_data`, or
  `orbit_fit_statistics`
- cometary elements via `M.COM`
- Cartesian elements via `M.CAR`
- optional Keplerian elements via `M.KEP`
- individual fitted quantities such as `M.q`, `M.e`, `M.x`, or `M.vx`

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
pip install -e .[test]
```

## Main API

### `MPCORB`

The main entry point is `mpc_orb.parse.MPCORB`.

```python
from mpc_orb.parse import MPCORB

M = MPCORB("path/to/file.json")
```

When you instantiate `MPCORB`, the package:

1. interprets the input as either a JSON filepath or a Python dictionary
2. validates the content against the packaged schema
3. exposes the parsed content as object attributes

You can also instantiate an empty object and parse later:

```python
from mpc_orb.parse import MPCORB

M = MPCORB()
M.parse("path/to/file.json")
```

### `validate_mpcorb`

Validation lives in `mpc_orb.validate_mpcorb`.

```python
from mpc_orb import validate_mpcorb

validate_mpcorb.validate_mpcorb("path/to/file.json")
```

If the input is valid, the function returns `True`. If it is not valid, it
raises an exception from the validation layer.

### `describe`

`MPCORB.describe()` looks up a field in the schema and returns a compact
description of the field and its units when available.

```python
info = M.describe("q")
print(info)
```

This is especially useful when exploring less familiar fields or when building
tools on top of the schema.

## Quick Start

```python
from mpc_orb.parse import MPCORB
from mpc_orb import validate_mpcorb

json_path = "tests/jsons/pass_mpcorb/2012HN13_mpcorb_yarkovsky.json"

# Validate first if you want an explicit validation step
validate_mpcorb.validate_mpcorb(json_path)

# Parse into a Python object
M = MPCORB(json_path)

# Top-level metadata
print(M.designation_data["iau_name"])
print(M.software_data["mpcorb_version"])

# Cometary elements
print(M.COM.q["val"], M.COM.q["unc"])
print(M.COM.e["val"], M.COM.e["unc"])

# Cartesian elements
print(M.CAR.x["val"], M.CAR.x["unc"])
print(M.CAR.vx["val"], M.CAR.vx["unc"])

# Convenience aliases also exist on the top-level object
print(M.q["val"])
print(M.x["val"])

# Full covariance matrix assembled from the triangular covariance terms
print(M.CAR.covariance_array.shape)

# Optional Keplerian elements may be present in some files
if hasattr(M, "KEP"):
    print(M.KEP.a["val"])
```

## Data Model

An `MPCORB` instance exposes both raw sections from the JSON and some
convenience structures created during parsing.

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

`COM`, `CAR`, and optional `KEP` are represented as `COORD` objects. Each one
includes:

- `coefficient_names`
- `coefficient_values`
- `coefficient_uncertainties`
- `eigenvalues`
- `covariance`
- `covariance_array`
- `element_dict`

The individual fitted quantities are also exposed as attributes. For example:

- `M.COM.q`
- `M.CAR.x`
- `M.KEP.a`

Each of these is a dictionary with `val` and `unc` keys.

## Accepted Inputs

Most public functions in this package accept either:

- a string path to a JSON file on disk
- a Python `dict` containing the JSON content

That behavior is implemented in `interpret.py` and is used by both the parser
and validator.

## Schema Files And Version Selection

The packaged schema files live in `mpc_orb/schema_json/`.

Validation is version-aware: `validate_mpcorb.validate_mpcorb()` reads
`software_data["mpcorb_version"]` from the input JSON and loads the matching
schema file from the package.

If you call `load_schema()` directly with no version, the package loads the
`latest` schema alias:

```python
from mpc_orb import validate_mpcorb

schema = validate_mpcorb.load_schema()
```

## Examples And Demo Material

The repository includes a few places to look for working examples:

- `mpc_orb/demo_json/` contains sample JSON files
- `mpc_orb/bin/demo.py` provides a simple command-line demo
- `demos/Example_parse_mpcorb_json.ipynb` shows interactive usage

After installation, the demo script is also exposed as:

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

## Package Layout

- `mpc_orb/parse.py`: parser and `MPCORB` class
- `mpc_orb/validate_mpcorb.py`: schema loading and validation helpers
- `mpc_orb/interpret.py`: input normalization for filepaths and dictionaries
- `mpc_orb/schema_json/`: packaged JSON schema files
- `mpc_orb/demo_json/`: sample orbit JSON files
- `tests/`: parser and validation tests
