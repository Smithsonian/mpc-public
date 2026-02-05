# Building digest2

## Download / Clone

The `digest2` source code is available as part of the `mpc-public` repository.
The `mpc-public` download page is: https://github.com/Smithsonian/mpc-public, and it can be cloned
with:

```sh
git clone https://github.com/Smithsonian/mpc-public.git
```

## Build

If you downloaded the `mpc-public` repository as a `.zip` or `.tar.gz` file, unpack it. On most
Linux-like systems, this can be done with `unzip <filename>` or `tar -xf <filename>`.

The `mpc-public` root directory will contain 3 subdirectories: `digest2`, `docs-public` and `mpc-orb`.
For reference, here's a quick view of the `mpc-public` repo layout, with a focus on the `digest2`
folder structure:

```
mpc-public/
|-- digest2/
|   |-- digest2/        <-- You are here: mpc-public/digest2/digest2/BUILDING.md
|   |-- population/
|   `-- NEOCP_filters/
|-- docs-public/
`-- mpc-orb/
```

From the `mpc-public` root directory, `cd` into the `digest2` directory:

```sh
cd digest2
```

The `digest2` top-level directory contains 3 subdirectories: `digest2`, `NEOCP_filters` and `population`.
The `digest2` directory contains the latest version of the source code and a `Makefile`.
The `population` directory contains the population data used by `digest2`.

Type `make`, and a `digest2` executable should be built in the current directory. The `Makefile` is
simplistic and may take minor modifications to work on your system; detailed instructions can be
found in the "Installation and requirements" section of the `digest2` top-level [README.md](../README.md)

## Model

Digest2 also requires a Solar System model file.  A model file, called `digest2.model` can be
found in the `population` directory. This file is updated periodically from the Minor Planet Center's `MPCORB.DAT` file.
Copy the `digest2.model`, `digest2.model.csv` and `MPC.config` files to the same directory as the `digest2` executable.

## Initial program checkout

Type "digest2 sample.obs" and you should get output similar to this:

```
Desig.    RMS Int NEO N22 N18 Other Possibilities
NE00030  0.15 100 100  37   0
NE00199  0.56  98  97  17   0 (MC 2) (JFC 1)
NE00269  0.42  18  18   3   0 (MC 9) (Hun 4) (Pho 27) (MB1 <1) (Han <1) (MB2 30) (MB3 12) (JFC 1)
```

The Internet conection is used only to get a copy of observatory parallax data
from the Minor Planet Center.  An Internet connection is not otherwise used
so it is not required, but without an Internet connection you will need to
otherwise get a copy of the Minor Planet Center's observatory codes file via the
[Observatory Codes API](https://www.minorplanetcenter.net/mpcops/documentation/obscodes-api/)
and place it in the current directory with the file name `digest2.obscodes`.

## Installation and configuration

See file OPERATION.md.
