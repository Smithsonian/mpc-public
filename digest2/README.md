# digest2

NEO orbit classification from short-arc astrometric tracklets.
Available as both a C command-line tool and a pip-installable Python package.

digest2 is a fast short-arc orbit classifier for minor planets, primarily used to identify Near-Earth Object (NEO) candidates from astrometric tracklets (groups of 2+ observations of the same object over a short time). It has been in operational use at the Minor Planet Center for over 15 years and is a key component of the NEO discovery workflow.

Given a set of observations, digest2 outputs a score (0-100) for each of 14 orbit classes, representing the pseudo-probability that the object belongs to that class. Objects scoring D2 >= 65 for the NEO class are posted to the NEO Confirmation Page (NEOCP) for follow-up.

**References:**
- Keys et al. 2019, "The digest2 NEO Classification Code" (PASP 131, 064501) -- [arXiv:1904.09188](https://arxiv.org/abs/1904.09188)
- Shober, Cloete, Veres 2023, "Improvement of digest2 NEO Classification Code" -- [arXiv:2309.16407](https://arxiv.org/abs/2309.16407)

**Authors:** Sonia Keys (original), with contributions from Carl Hergenrother, Robert McNaught, David Asher. ADES support added by Richard Cloete and Peter Veres.

**License:** Public domain.

---

## Python Package (recommended)

```bash
pip install digest2
```

```python
from digest2 import Digest2

with Digest2() as d2:
    results = d2.classify_file("observations.obs")
    for r in results:
        print(r.designation, r.noid.NEO, r.noid.MB1)
```

The Python package wraps the C scoring engine via a CPython extension. No libxml2 or pthreads required -- XML parsing is done in Python, and scoring is single-threaded. Cross-platform wheels are available for Linux, macOS, and Windows.

### Python API

- **`Digest2(model_path=None, config_path=None, obscodes_path=None, repeatable=True, no_threshold=False)`** -- Stateful classifier; auto-discovers bundled model data. Set `no_threshold=True` to disable per-observation RMS ceiling clamping.
- **`d2.classify_tracklet(observations)`** -- Classify a list of `Observation` objects. Returns `ClassificationResult`.
- **`d2.classify_file(filepath)`** -- Classify all tracklets in an MPC 80-col or ADES XML file. Returns `List[ClassificationResult]`.
- **`classify(input, ...)`** -- One-shot convenience function.
- **`parse_mpc80(line)`** / **`parse_mpc80_file(path)`** -- Parse MPC 80-column observations.
- **`parse_ades_xml(path)`** -- Parse ADES XML observations.
- **`digest2.filters`** -- NEOCP threshold filtering tools (requires `pip install digest2[filters]`).

### Development Setup

```bash
cd digest2
pip install -e '.[test]'

# Download observatory codes (one-time)
curl -o digest2/digest2.obscodes https://minorplanetcenter.net/iau/lists/ObsCodes.html

# Run tests
pytest tests/ -v
```

### Python Package Structure

```
src/digest2/
├── __init__.py           # Package init, imports Digest2, classify, Scores, ClassificationResult
├── _extension.c          # CPython C extension (low-level bindings to d2lib)
├── core.py               # High-level API: Digest2 class, classify() function
├── result.py             # ClassificationResult and Scores dataclasses
├── observation.py        # Observation dataclass, MPC80/ADES parsers
├── model.py              # Model/obscodes/config path resolution
├── filters.py            # NEOCP filter tools (from NEOCP_filters/)
└── data/
    └── MPC.config        # Bundled per-site observatory errors
```

### C Library API (d2lib)

The files `d2lib.h` / `d2lib.c` provide a clean, non-threaded library interface used by the Python extension:

- `d2_init(model_csv, obscodes)` -- Load model and observatory data
- `d2_score_observations(obs, n, classes, n_classes, is_ades)` -- Score a tracklet
- `d2_cleanup()` -- Release resources
- `d2_configure()` -- Set observatory errors, repeatable mode, noThreshold flag
- No libxml2 or pthreads dependency (XML parsing done in Python)

### Key Design Decisions

- **Existing CLI is unchanged.** `make` in `digest2/digest2/` still builds the same binary.
- **Preprocessor guards** (`D2_NO_LIBXML`, `D2_NO_REGEX`) allow building without libxml2/regex.
- **Global state is managed** by `d2_init()`/`d2_cleanup()` -- single-threaded library mode.
- **Band correction** matches C code exactly (common.c `updateMagnitude`).
- **MJD calculation** uses C-style truncation-toward-zero integer division.

---

## C Command-Line Tool

### Building from Source

Requirements:
- C99-capable C compiler (e.g., `gcc` or `clang`)
- `make`
- `libxml2` development headers (`libxml2-dev` or `libxml2-devel`)
- Optional: internet connection to download latest observatory codes from the MPC website.

```bash
cd digest2/digest2
make                          # Produces the `digest2` executable
```

Ensure the runtime data files are alongside the executable:
- `digest2.model` (or `digest2.model.csv`), and `MPC.config` (found under `digest2/population/`; updated versions can be copied in when available).

Platform notes:
- The provided `Makefile` is minimal and may require small tweaks for non-Linux platforms (see `digest2/digest2/BUILDING.md` for details).
- **libxml2** is required for ADES XML parsing. Install the development package for your platform:
  - Debian/Ubuntu: `sudo apt-get install libxml2 libxml2-dev`
  - RHEL/CentOS/Fedora: `sudo dnf install libxml2 libxml2-devel`
  - macOS: `brew install libxml2` (ensure headers are on your include path via `pkg-config`)

### Usage

```bash
# MPC 80-column format
./digest2 sample.obs

# ADES XML format
./digest2 sample.xml

# With config file (per-observatory errors)
./digest2 -c MPC.config sample.obs

# From stdin
cat sample.obs | ./digest2 -

# Generate binary model from CSV (faster subsequent loads)
./digest2 -m digest2.model
```

Run `./digest2 sample.obs` to verify the build. Expected output (small differences may occur):
```
Desig.    RMS Int NEO N22 N18 Other Possibilities
K16S99K  0.73   0   2   1   0 (MC 2) (MB1 93) (MB2 3) (JFC <1)
```

Notes:
- If you have an internet connection, `digest2` will download the latest observatory parallax data from the Minor Planet Center. Otherwise, download `ObsCodes.html` and place it in the current directory as `digest2.obscodes`.
- To execute from a different directory, use the `-p` option: `./digest2 some.obs -p '/path/to/data'`.
- Run `./digest2 --help` for full command-line help.
- More detailed options can be found in [digest2/OPERATION.md](digest2/OPERATION.md).

### Input Formats

1. **MPC 80-column** (`.obs`): Fixed-width format with packed designation, date, RA/Dec, magnitude, observatory code
2. **ADES XML** (`.xml`): Rich format with per-observation uncertainties (rmsRA, rmsDec), roving/satellite observer support

### Config File Keywords

| Keyword | Description |
|---------|-------------|
| `headings`/`noheadings` | Toggle column headers in output |
| `rms` | Output great-circle RMS of tracklet |
| `rmsPrime` | Output RMS from ADES-provided uncertainties |
| `raw` | Output raw population scores |
| `noid` | Output no-ID scores (default) |
| `repeatable`/`random` | Deterministic vs stochastic Monte Carlo seeding |
| `obserr` | Default observational error (arcsec), default 1.0 |
| `obserrXXX` | Per-observatory error (e.g., `obserrF51=0.3`) |
| `poss` | Show "Other Possibilities" column |
| `noThreshold` | Accept ADES uncertainties without floor/ceiling clamping |

---

## Algorithm Overview

1. **Motion vector & photometry:** Computes a motion vector from the first and last observation, and a composite V magnitude from available photometry (default 21 if none).

2. **Statistical ranging:** Generates many trial orbits consistent with the observed motion, each with an absolute magnitude (H) consistent with the apparent brightness.

3. **Histogram binning:** Each trial orbit is located in a 4D binned model of the Solar System (dimensions: q, e, i, H). Bins are tagged as "reachable" for each orbit class.

4. **Iterative search:** Orbits are generated to explore the full solution space, terminating when diminishing returns in discovering new bins.

5. **Population scoring (raw):** The population of tagged bins for a given class, divided by the total population of all tagged bins, gives the raw score (x100).

6. **No-ID scoring (noid):** Same as raw, but uses the estimated *undiscovered* population (total minus known objects with sky uncertainty < 1 arcmin). This is the default score and represents the probability that an *unidentified* tracklet belongs to a class.

### Model Dimensions

The population histogram is binned in 4 dimensions:
- **q** (perihelion): 29 bins
- **e** (eccentricity): 8 bins
- **i** (inclination): 11 bins
- **H** (absolute magnitude): 18 bins

Total: 29 x 8 x 11 x 18 = 45,936 bins per class, times 15 classes.

### Orbit Classes (14 + "MPC Interest")

| Abbr | Description |
|------|-------------|
| Int  | MPC Interest (q<1.3 OR e>0.5 OR i>=40 OR Q>10) |
| NEO  | Near-Earth Object (q < 1.3 AU) |
| N22  | NEO with H <= 22 |
| N18  | NEO with H <= 18 |
| MC   | Mars Crosser |
| Hun  | Hungaria group |
| Pho  | Phocaea group |
| MB1  | Inner Main Belt |
| Pal  | Pallas group |
| Han  | Hansa group |
| MB2  | Middle Main Belt |
| MB3  | Outer Main Belt |
| Hil  | Hilda group |
| JTr  | Jupiter Trojan |
| JFC  | Jupiter Family Comet |

---

## NEOCP Filters

Post-processing tools that apply threshold-based filtering to digest2 output to separate likely NEOs from non-NEOs, using the methods documented in [Veres et al. (2025)](https://arxiv.org/abs/2505.11910).

**Requirements:** Python 3.6+, pandas (`pip install pandas` or `pip install digest2[filters]`)

**Tools:**
- `find_filter.py` -- Trains optimal per-class thresholds from labeled NEOCP data. Reads a digest2 CSV and produces `optimal_thresholds.json`.
- `neocp_filter.py` -- Applies thresholds to new digest2 output to flag likely non-NEOs for removal from NEOCP.

**Sample data:**
- `digest_data_19-24.csv` -- Training data (2019-2023 NEOCP)
- `digest_data_24.csv` -- Test data (2024 NEOCP)
- `optimal_thresholds.json` -- Pre-computed thresholds

### End-to-End Example

1. Create a config file `digest2.conf` in the directory where the `digest2` binary lives:

    ```
    repeatable
    norms
    raw
    noid
    Int
    NEO
    MC
    Hun
    Pho
    MB1
    Pal
    Han
    MB2
    MB3
    Hil
    JTr
    JFC
    ```

2. Run `digest2` on an ADES XML file and save the output:

    ```bash
    ./digest2 sample.xml -c digest2.conf > sample.digest2
    ```

3. Convert the output to the CSV format expected by the filter tools:

    ```python
    with open("sample.digest2", "r") as infile:
        lines = infile.readlines()[2:]  # skip header lines

    output_lines = []
    for line in lines:
        fields = line.strip().split()
        fields.append("0")  # Add class column (placeholder)
        output_lines.append(",".join(fields))

    with open("sample.digest2.csv", "w") as outfile:
        outfile.write("trksub,Int1,Int2,Neo1,Neo2,MC1,MC2,Hun1,Hun2,Pho1,Pho2,"
                      "MB1_1,MB1_2,Pal1,Pal2,Han1,Han2,MB2_1,MB2_2,MB3_1,MB3_2,"
                      "Hil1,Hil2,JTr1,JTr2,JFC1,JFC2,class\n")
        for line in output_lines:
            outfile.write(line + "\n")
    ```

4. Apply the filter:

    ```bash
    python NEOCP_filters/neocp_filter.py sample.digest2.csv NEOCP_filters/optimal_thresholds.json
    ```

    If the input contains non-NEO tracklets, `neocp_filter.py` will output those flagged as likely non-NEOs. NEO tracklets produce no output.

---

## Directory Structure

```
digest2/
├── digest2/                 # C source code and build system
│   ├── Makefile             # Build: `make` produces `digest2` executable
│   ├── digest2.c            # Main program: CLI, threading, I/O orchestration
│   ├── d2math.c             # Core algorithm: orbit generation, scoring, statistical ranging
│   ├── d2cli.c              # Command-line parsing and config file reading
│   ├── d2model.c            # Population model: orbit class definitions, bin partitions
│   ├── d2modelio.c          # Model I/O: read CSV, read/write binary model
│   ├── d2mpc.c              # MPC 80-column format parser, observatory code loading
│   ├── d2ades.c             # ADES XML format parser (uses libxml2)
│   ├── common.c             # Shared utilities (obscode parsing, magnitude conversion)
│   ├── digest2.h            # Main header: observation, tracklet, perClass structs
│   ├── d2model.h            # Model dimensions: QX=29, EX=8, IX=11, HX=18; 15 classes
│   ├── d2ades.h             # ADES optical observation struct
│   ├── common.h             # Shared function declarations
│   ├── ALGORITHM.md         # Algorithm description
│   ├── BUILDING.md          # Build instructions
│   ├── OPERATION.md         # Usage, config file format, orbit class list
│   ├── sample.obs           # Sample MPC 80-column input
│   ├── sample.xml           # Sample ADES XML input
│   └── MPC.config -> ../population/MPC.config
│
├── population/              # Solar System population model data
│   ├── digest2.model.csv    # 4D histogram of SS populations (q, e, i, H bins)
│   ├── MPC.config           # Config with per-observatory observational errors
│   ├── README.md
│   └── make_population/     # Tools to regenerate model from SSM + astorb.dat
│       ├── s3mbin.c         # Processes Pan-STARRS Synthetic Solar System Model
│       ├── muk.c            # Combines s3m.dat + astorb.dat -> digest2.model.csv
│       └── README.md
│
├── NEOCP_filters/           # Post-processing filters for NEO/non-NEO classification
│   ├── find_filter.py       # Derives optimal thresholds from labeled digest2 output
│   ├── neocp_filter.py      # Applies thresholds to flag likely non-NEOs
│   ├── optimal_thresholds.json  # Pre-computed thresholds
│   ├── digest_data_19-24.csv    # Training data (2019-2023 NEOCP)
│   ├── digest_data_24.csv       # Test data (2024 NEOCP)
│   ├── MPC.config
│   └── README.md
│
├── src/digest2/             # Python package source
├── tests/                   # Python package tests
├── pyproject.toml           # Python package build configuration
└── README.md                # This file
```

## Key Data Structures (C)

- **`observation`** -- Single astrometric observation: MJD, RA/Dec (radians), V magnitude, site index, rmsRA/rmsDec
- **`tracklet`** -- Group of observations of one object: designation, observation list, motion vector, scoring arrays, per-class results
- **`perClass`** -- Per-class scoring data: raw/noID scores, tagged bin arrays, population sums
- **`site`** -- Observatory parallax constants and observational error

## Dependencies

- **C CLI:** C99 compiler, `libxml2` (for ADES XML parsing), pthreads, math library
- **Python package:** Python >= 3.8, C99 compiler for building from source (no libxml2 or pthreads needed)
- **Filters (optional):** pandas
- **Runtime data:** `digest2.model.csv`, `MPC.config`, `digest2.obscodes` (auto-downloaded from MPC)
