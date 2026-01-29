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
- Optional: internet connection to download latest list of observatory codes from the MPC website.

To build and install `digest2` (from the `mpc-public` repo root) run the following commands:
1. `cd digest2/digest2` — this is the directory containing the `Makefile` used by `make` to build `digest2`.
2. `make` — builds the `digest2` executable in the same directory.
3. Ensure the runtime data files are alongside the executable:
   - `digest2.model`, `digest2.model.csv`, and `MPC.config` (found under `digest2/population`; updated versions can be copied in when available).

#### Usage

Here we illustrate how to use `digest2`; more detailed options and be found in
[digest2/digest2/OPERATION.md](digest2/digest2/OPERATION.md). Run `./digest2 sample.obs` to verify
the build (sample observation file `sample.obs` is provided for testing). This should produce the
following output (small differences might occur):
```
Desig.    RMS Int NEO N22 N18 Other Possibilities
K16S99K  0.73   0   2   1   0 (MC 2) (MB1 93) (MB2 3) (JFC <1)
```

Notes:
- If the program cannot reach the Minor Planet Center to fetch observatory codes data, place a copy
  of `obscode.dat` as `digest2.obscodes` in the same directory as the executable.
- The provided `Makefile` is minimal and may require small tweaks for non-Linux platforms (see
  `digest2/digest2/BUILDING.md` for details).
- `libxml2`: the code uses libxml2 for XML parsing (ADES input). Install the development package from
  your platform: on Debian/Ubuntu `sudo apt-get install libxml2 libxml2-dev`; on RHEL/CentOS/Fedora 
  `sudo dnf install libxml2 libxml2-devel`; on macOS `brew install libxml2` (then ensure its headers 
  are on your include path via Homebrew’s `pkg-config`).
- Command-line help can be obtained doing `./digest2 --help`.

#### `digest2/NEOCP_filters`:

This subfolder contains tools and sample data for filtering digest2 output to separate likely NEOs from
non‑NEOs with the methods documented in “[Veres et al. (2025)](https://arxiv.org/abs/2505.11910)” (Vereš, Cloete, Payne, Loeb; arXiv:2505.11910).

##### Installation and requirements

In order to use the `NEOCP_filters` code, a `python` installation (3.6+) with an environment where `pandas`
is available is required. The `pandas` package can be installed in a python environment e.g. using
`pip` running the following command: `python -m pip install pandas`. We note that in order to use
`find_filter.py` and `neocp_filter.py`, the output from `digest2` has to be converted to the
appropriate CSV format expected by these tools.

Example data file `digest_data_19-24.csv` includes digest2 output in CSV format for NEOCP data
collected between 2019-2023; data file `digest_data_24.csv` includes digest2 output in CSV format for
NEOCP data collected during 2024. Derived thresholds following the methods from the paper are found
in `optimal_thresholds.json`.

##### Code tools

- `find_filter.py`: reads a digest2 CSV (e.g., `digest_data_19-24.csv`) and produces a JSON threshold
  model `optimal_thresholds.json`. Example:
  ```
  python3 find_filter.py digest_data_19-24.csv
  ```
- `neocp_filter.py`: applies the JSON model to new digest2 output to select assumed non‑NEOs. Example:
  ```
  python3 neocp_filter.py digest_data_24.csv optimal_thresholds.json
  ```

##### Example

Add the configuration file `digest2.conf` in the directory where the `digest2` binary lives, with the
following contents:

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

Then, run `digest2` on an ADES XML observations file, e.g. `sample.xml`, and save the results into
`sample.digest2`:

```sh
./digest2 sample.xml -c my_digest2.conf > sample.digest2
```

Next, in a python session, run:
```python
with open("sample.digest2", "r") as infile:
    lines = infile.readlines()[2:]  # skip header lines

output_lines = []
for line in lines:
    fields = line.strip().split()
    fields.append("0")  # Add class column with value 0, not used
    output_lines.append(",".join(fields))

with open("sample.digest2.csv", "w") as outfile:
    outfile.write("trksub,Int1,Int2,Neo1,Neo2,MC1,MC2,Hun1,Hun2,Pho1,Pho2,MB1_1,MB1_2,Pal1,Pal2,Han1,Han2,MB2_1,MB2_2,MB3_1,MB3_2,Hil1,Hil2,JTr1,JTr2,JFC1,JFC2,class\n")
    for line in output_lines:
        outfile.write(line + "\n")
```

This will produce the file `sample.digest2.csv`, which has converted the `digest2` output file
`sample.digest2` to the CSV format expected by `neocp_filter.py`. This means we can now run
`neocp_filter.py` on `sample.digest2.csv` as follows:

```sh
python neocp_filter.py ../digest2/sample.digest2.csv optimal_thresholds.json
```

In this example, we have used `sample.xml`, which corresponds to an NEO tracklet. Thus, in this
case, `neocp_filter.py` produces no output. Otherwise, if the input observations file has non-NEO
tracklets, then `neocp_filter.py` will output the tracklets which have a high likelihood of
corresponding to non-NEO tracklets, as detailed by Veres et al. (2025).

### docs-public
Last Update: 2026-01-29
 - `docs-public` provides a landing page for the MPC's documentation website, 
[https://docs.minorplanetcenter.net/](https://docs.minorplanetcenter.net/). 

