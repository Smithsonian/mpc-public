# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the Minor Planet Center's public repository containing:
- **mpc_orb**: Python package for standardized orbit data exchange using JSON format
- **docs-public**: MkDocs-based documentation site deployed to https://docs.minorplanetcenter.net/

## Common Commands

### mpc_orb (Python Package)

```bash
# Development setup
conda create -n mpc-orb-public python=3.11
conda activate mpc-orb-public
cd mpc_orb
python3 -m pip install -e '.[test]'

# Run tests (from mpc_orb directory)
pytest -v

# Run a single test file
pytest tests/test_parse.py -v

# Run a single test
pytest tests/test_parse.py::test_MPCORB_A -v
```

### docs-public (Documentation Site)

```bash
# Install dependencies
pip install mkdocs mkdocs-material mkdocs-jupyter

# Local development (from docs-public directory)
mkdocs serve
# Then visit http://127.0.0.1:8000/index.html

# Deploy to public site
mkdocs gh-deploy
```

## Architecture

### mpc_orb Package Structure

- `mpc_orb/parse.py` - Main `MPCORB` class for parsing mpc_orb.json orbit files
- `mpc_orb/validate_mpcorb.py` - JSON schema validation
- `mpc_orb/interpret.py` - Handle dict/filepath input interpretation
- `mpc_orb/schema_json/` - JSON schema definitions (versions 0.1-0.6, latest symlink)
- `mpc_orb/demo_json/` - Example orbit JSON files
- `tests/jsons/` - Test data with pass/fail samples

### docs-public Structure

- `docs/mpc-ops-docs/` - MPC operations documentation pages
- `docs/tutorials/notebooks/` - Jupyter notebook API tutorials
- `docs/javascript/` - Custom JS for notebook downloads
- `mkdocs.yml` - Site configuration with Material theme

## Release Process (PyPI)

1. Increment version in `mpc_orb/pyproject.toml`
2. Go to https://github.com/Smithsonian/mpc-public
3. Create a new release with tag `vX.Y.Z`
4. GitHub Action automatically publishes to PyPI

## CI/CD

- **mpc_orb_pytest.yml**: Runs tests across Python 3.6-3.11 on Ubuntu, macOS, Windows
- **release.yml**: Publishes to PyPI on release creation

## Key Dependencies

- mpc_orb requires: numpy<2.0.0, jsonschema, json5
- Python >= 3.6
