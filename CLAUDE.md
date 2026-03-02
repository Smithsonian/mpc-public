# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the Minor Planet Center's public repository containing:
- **mpc_orb**: Python package for standardized orbit data exchange using JSON format
- **docs-public**: MkDocs-based documentation site deployed to https://docs.minorplanetcenter.net/
- **MIGRATION_TRACKER.md**: Tracks the status of all legacy page migrations (see `/migrate-docs-project-man` skill)

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
- `docs/tutorials/submission_tutorials.md` - Links to submission-related notebooks
- `docs/tutorials/api_tutorials.md` - Links to API tutorial notebooks
- `docs/javascript/` - Custom JS for notebook downloads
- `mkdocs.yml` - Site configuration with Material theme

### Tutorial Notebook Conventions

- **Naming**: `mpc_tutorial_api_*.ipynb` for API tutorials, `mpc_tutorial_*.ipynb` for general tutorials
- **Structure**: Title markdown → Import section → Sample data download (using `tempfile`/`atexit` for cleanup) → Examples (success then failure cases) → Summary
- **mkdocs-jupyter config**: `execute: false`, `include_source: true` — notebooks are not executed during build
- **Sample ADES files**: Available at `https://data.minorplanetcenter.net/media/ades/goodsubmit.xml.txt` and `goodsubmit.psv.txt`
  - These use ADES v2017; the current `iau-ades` package (v0.1.1) validates against v2022
  - When using these samples, update: `version` attribute to `2022`, remove `+` prefix from `<ra>`/`<dec>` values in XML, fix `+` prefixed values in PSV

### mpc_orb Package Quirks

- **`M.CAR.eigenvalues` is misleading**: The `eigenvalues` attribute stored in the JSON (and exposed by `MPCORB`) does **not** correspond to eigenvalues of `M.CAR.covariance_array`. Use `np.linalg.eigvalsh(M.CAR.covariance_array)` to compute the actual covariance eigenvalues.
- **Rebound unit mismatch**: MPC Cartesian elements use AU and AU/day, but Rebound's default Horizons units use yr/(2π) for time. When combining MPC state vectors with Horizons-loaded planets, set `sim.units = ('AU', 'day', 'Msun')` before adding any particles to ensure consistent units.

### iau-ades Package Quirks

The `iau-ades` pip package is used for local ADES validation and PSV/XML conversion:

- **`psvtoxml` global state bug**: Calling `psvtoxml()` twice in the same Python process causes `"ElemenStack is too short to pop"` error. Workaround: `importlib.reload(ades.psvtoxml)` before the second call.
- **`valsubmit` output**: Writes results to `valsubmit.file` in CWD (not returned as a value); detailed error tracebacks print to stdout.
- **Schema version**: The package validates against ADES v2022 schema only (`version="2022"`).

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

## Documentation Migration Notes

### Completed Migrations

The following documentation pages have been migrated from MPC legacy pages into local markdown:

**designations/** (migrated from `designations.md`):

- `designations/index.md` - Index page with button links to local pages, text links to external/dynamic resources
- `designations/provisional-designations.md` - Consolidated from `mpcops/documentation/provisional-designation-definition/` and `/iau/info/OldDesDoc.html`
- `designations/temporary-designations.md` - From `/iau/info/TempDesDoc.html`
- `designations/how-asteroids-are-named.md` - From `/iau/info/HowNamed.html`
- `designations/cometary-designation-system.md` - From `/iau/lists/CometResolution.html`
- `designations/packed-designations.md` - Consolidated from `/iau/info/PackedDes.html` + extended packed format from mpcops page
- `designations/packed-dates.md` - From `/iau/info/PackedDates.html`
- `designations/dual-status-objects.md` - From `/iau/lists/DualStatus.html`

**identifications/** (migrated from `identifications.md`):

- `identifications/index.md` - Full overview content from `mpcops/documentation/identifications/` + links
- `identifications/submission-format.md` - From `mpcops/documentation/identifications/submission-format/`
- `identifications/acceptance-criteria.md` - From `mpcops/documentation/identifications/additional/`

**astrometry/** (migrated from `/iau/info/Astrometry.html`):

- `astrometry/getting-started.md` - Getting started with astrometry submissions
- `astrometry/observatory-codes.md` - Observatory codes overview
- `astrometry/reporting-observations.md` - How to report observations
- `astrometry/discoveries-and-credit.md` - Discovery credit and procedures
- `astrometry/mpc-processing.md` - How the MPC processes observations

**data-and-services/**:

- `data-and-services/non-english-characters.md` - From `/iau/info/NonEnglish.html`

### Migration Conventions

- Pages with many links become sub-folders with an `index.md` and individual content pages
- Button-style links (using `<div class="contents-grid">`) point to locally-hosted pages within mpc-public
- Standard text links point to external/dynamic/service pages that remain on the legacy MPC site
- MPEC pages (e.g. `https://minorplanetcenter.net/mpec/...`) are never imported
- Service/API endpoints are never imported
- Auto-generated data lists (e.g. MPNames, NumberedMPs) are left as external links
