# `digest2`

This folder contains the `digest2` code, as well as the `NEOCP_filters` derived from `digest2`
results. Further details can be found, respectively, in [digest2/README.md](digest2/README.md)
and [NEOCP_filters/README.md](NEOCP_filters/README.md)

## Installation: building `digest2` from source

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

## Usage

Here we illustrate how to use `digest2`; more detailed options and be found in
[OPERATION.md](digest2/OPERATION.md). Run `./digest2 sample.obs` to verify
the build (sample observation file `sample.obs` is provided for testing). This should produce the
following output (small differences might occur):
```
Desig.    RMS Int NEO N22 N18 Other Possibilities
K16S99K  0.73   0   2   1   0 (MC 2) (MB1 93) (MB2 3) (JFC <1)
```

Notes:
- If you have internet connection `digest2` will download the latest observatory parallax data from
  the Minor Planet Center. If no internet connection is available, you will need to download the
  `obscode.dat` file from the Minor Planet Center and place it in the current directory with the name
  `digest2.obscodes`.
- The provided `Makefile` is minimal and may require small tweaks for non-Linux platforms (see
  `digest2/digest2/BUILDING.md` for details).
- `libxml2`: the code uses libxml2 for XML parsing (ADES input). If not yet installed: install the
  development package for your platform: on Debian/Ubuntu `sudo apt-get install libxml2 libxml2-dev`;
  on RHEL/CentOS/Fedora `sudo dnf install libxml2 libxml2-devel`; on macOS `brew install libxml2`
  (then ensure its headers are on your include path via Homebrew’s `pkg-config`).
- Command-line help can be obtained doing `./digest2 --help`.
- To execute from a path different from the path where the `digest2` binary lives, the `-p` option
  can be used, e.g.: `/full/path/to/digest2/folder/digest2 some.obs -p '/full/path/to/digest2/folder'`.
  Note that the path to the `digest2` binary and the path provided in the `-p` do not need to match.

## `digest2/NEOCP_filters`:

This subfolder contains tools and sample data for filtering digest2 output to separate likely NEOs from
non‑NEOs with the methods documented in [Veres et al. (2025)](https://arxiv.org/abs/2505.11910).

## Installation and requirements

In order to use the `NEOCP_filters` code, a `python` installation (3.6+) with an environment where `pandas`
is available is required. The `pandas` package can be installed in a python environment e.g. using
`pip` running the following command: `python -m pip install pandas`. We note that in order to use
`find_filter.py` and `neocp_filter.py`, the output from `digest2` has to be converted to the
appropriate CSV format expected by these tools.

Example data file `digest_data_19-24.csv` includes digest2 output in CSV format for NEOCP data
collected between 2019-2023; data file `digest_data_24.csv` includes digest2 output in CSV format for
NEOCP data collected during 2024. Derived thresholds following the methods from the paper are found
in `optimal_thresholds.json`.

## Code tools

- `find_filter.py`: reads a digest2 CSV (e.g., `digest_data_19-24.csv`) and produces a JSON threshold
  model `optimal_thresholds.json`. Example:
  ```
  python3 find_filter.py digest_data_19-24.csv
  ```
- `neocp_filter.py`: applies the JSON model to new digest2 output to select assumed non‑NEOs. Example:
  ```
  python3 neocp_filter.py digest_data_24.csv optimal_thresholds.json
  ```

## Example

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
being non-NEO tracklets, as detailed by Veres et al. (2025).
