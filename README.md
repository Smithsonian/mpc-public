# mpc-public

An over-arching repository to hold various publicly-released pieces of code written by the MPC

Notes for MPC staff/developers can be found in *DEVELOPER_NOTES.md*

## Current contents 

### mpc_orb
Last Update: 2025-02-25
 - Introduction of a new version: 0.5
 - Documentation and code related to a standardized format for the exchange of data on the *best-fit orbit* for solar-system bodies. 
 - The format uses JSON files for the exchange of data, and is refered to as the *mpc_orb.json* format.
 - Documentation is also available on the (https://minorplanetcenter.net/mpcops/documentation/mpc-orb-json/)[MPC Documentation page]
 - The *mpc_orb* repository includes:
    - json-schema files to define the standard;
    - sample orbit files in the format;
    - python code to parse & validate example orbit files.

### digest2
Last Update: 2025-11-21
 - XML-enhanced repository of digest2 code, population model and the configuration files.

#### Installation: building `digest2` from source

Requirements:
- C99-capable C compiler (e.g., `gcc` or `clang`)
- `make`
- `libxml2` development headers (`libxml2-dev` or `libxml2-devel`)

To build and install `digest2` (from the `mpc-public` repo root) run the following commands:
1. `cd digest2/digest2` — this is the directory containing the `Makefile` used by `make` to build `digest2`.
2. `make` — builds the `digest2` executable in the same directory.
3. Ensure the runtime data files are alongside the executable:
   - `digest2.model`, `digest2.model.csv`, and `MPC.config` (found under `digest2/population`; updated versions can be copied in when available).
4. Quick check: run `./digest2 sample.obs` to verify the build (sample observation file `sample.obs` is provided for testing).

Notes:
- If the program cannot reach the Minor Planet Center to fetch observatory parallax data, place a copy of `obscode.dat` as `digest2.obscodes` in the same directory as the executable.
- The provided `Makefile` is minimal and may require small tweaks for non-Linux platforms (see `digest2/digest2/BUILDING.md` for details).
- `libxml2`: the code uses libxml2 for XML parsing (ADES input). Install the development package from your platform: on Debian/Ubuntu `sudo apt-get install libxml2 libxml2-dev`; on RHEL/CentOS/Fedora `sudo dnf install libxml2 libxml2-devel`; on macOS `brew install libxml2` (then ensure its headers are on your include path via Homebrew’s `pkg-config`).

### docs-public
Last Update: 2026-01-29
 - `docs-public` provides a landing page for the MPC's documentation website, 
[https://docs.minorplanetcenter.net/](https://docs.minorplanetcenter.net/). 
