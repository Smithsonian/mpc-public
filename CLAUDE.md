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

**astrometry/** (migrated from `astrometry.md`):

- `astrometry/index.md` - Hub page with links to sub-pages and external services
- `astrometry/getting-started.md` - From `/iau/info/Astrometry.html` (equipment through timing sections)
- `astrometry/observatory-codes.md` - From `/iau/info/Astrometry.html` (observatory code sections)
- `astrometry/reporting-observations.md` - From `/iau/info/Astrometry.html` (reporting and checking sections)
- `astrometry/discoveries-and-credit.md` - From `/iau/info/Astrometry.html` (discoveries, coverage, naming sections)
- `astrometry/mpc-processing.md` - From `/iau/info/Astrometry.html` (processing and publication sections)

**observations/** (migrated from `observations.md`):

- `observations/index.md` - Hub page with button links to local pages, text links to external resources
- `observations/ades-format.md` - From `/iau/info/ADES.html`
- `observations/mpc1992-format.md` - From `/iau/info/ObsFormat.html`
- `observations/observational-details.md` - From `/iau/info/ObsDetails.html`
- `observations/command-line-submissions.md` - From `/iau/info/commandlinesubmissions.html`
- `observations/roving-observers.md` - From `/iau/info/RovingObs.html`
- `observations/telescope-details.md` - From `/iau/info/TelescopeDetails.html`
- `observations/catalogue-codes.md` - From `/iau/info/CatalogueCodes.html`
- `observations/reference-codes.md` - From `/iau/info/References.html`
- `observations/observation-notes.md` - From `/iau/info/ObsNote.html`
- `observations/tycho-tracker.md` - From `/mpcops/documentation/tycho-tracker/`

**orbits/** (migrated from `orbits.md`):

- `orbits/index.md` - Hub page with button links to local pages, text links to external resources
- `orbits/minor-planet-orbit-format.md` - From `/iau/info/MPOrbitFormat.html`
- `orbits/comet-orbit-format.md` - From `/iau/info/CometOrbitFormat.html`
- `orbits/satellite-orbit-format.md` - From `/iau/info/SatOrbitFormat.html`
- `orbits/orbit-format-overview.md` - From `/iau/info/OrbFormat.html`
- `orbits/orbit-notes.md` - From `/iau/info/OrbNote.html`
- `orbits/uncertainty-parameter.md` - From `/iau/info/UValue.html`
- `orbits/orbit-types.md` - From `/mpcops/documentation/orbit-types/`
- `orbits/object-types.md` - From `/mpcops/documentation/object-types/`
- `orbits/perturbers.md` - From `/iau/info/Perturbers.html`
- `orbits/ele220-format.md` - From `/mpcops/documentation/ele220/`
- `orbits/mpc-orb-json.md` - From `/mpcops/documentation/mpc-orb-json/`

**observatory-and-program-codes/** (migrated from `observatory-and-program-codes.md`):

- `observatory-and-program-codes/index.md` - Hub page with button links to local pages, text links to external resources
- `observatory-and-program-codes/observatory-codes-docs.md` - From `/iau/info/ObservatoryCodes.html`
- `observatory-and-program-codes/program-codes.md` - From `/mpcops/documentation/program-codes/`
- `observatory-and-program-codes/program-codes-policy.md` - From `/mpcops/documentation/program-codes-policy/`

**data-and-services/**:

- `data-and-services/non-english-characters.md` - From `/iau/info/NonEnglish.html`
- `data-and-services/submission-info.md` - From `/iau/info/TechInfo.html` (submission hub with links to migrated format docs)
- `data-and-services/neocp-notes.md` - From `/iau/NEO/NEOCPNotes.html`

**observations/** (additional):

- `observations/negative-observations.md` - From `/mpcops/documentation/negative-observations/`

**designations/** (additional):

- `designations/comet-naming-guidelines.md` - From `/iau/info/CometNamingGuidelines.html`

**data-and-services/** (additional):

- `data-and-services/lists.md` - Combined from `/iau/lists/Lists.html`, `/iau/lists/MPLists.html`, `/iau/lists/CometLists.html`

### Migration Conventions

- Pages with many links become sub-folders with an `index.md` and individual content pages
- Button-style links (using `<div class="contents-grid">`) point to locally-hosted pages within mpc-public
- Standard text links point to external/dynamic/service pages that remain on the legacy MPC site
- MPEC pages (e.g. `https://minorplanetcenter.net/mpec/...`) are never imported
- Service/API endpoints are never imported
- Auto-generated data lists (e.g. MPNames, NumberedMPs) are left as external links
