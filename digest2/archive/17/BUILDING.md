# Building digest2

## Download

The digest2 download page is http://bitbucket.org/mpcdev/digest2/downloads.
The page has three tabs, "Downloads," "Tags," and "Branches."  Click Tags.
Read across the row with the latest version; on the far right are options
"zip," "gz," "bz2."  Click one of them and your browser should download the
source archive.  Alternatively, with a right click your browser may give you
the option to name the archive file.  (By default the archive may be named
with a commit hash.)

## Build

In any case, you should be able to unpack the archive with a command like
`tar -xf <filename>` on most Linux-like systems.

Cd into the directory created by unpacking the archive and you should find
C source and related files.

Type `make`, and a `digest2` executable should be built in the current
directory.  (The Makefile is simplistic and may take minor modifications
to work on your system.)

## Model

Digest2 also requires a Solar System model file.  A model file can be
downloaded from the same download page mentioned above, but instead of the
"Tags" tab, use the "Downloads" tab.  There should be a file `d2model.tar.bz2`.
Download and unpack into the same directory with digest2.  You should find
two files, `digest2.model.csv` and `MPC.config`.

## Initial program checkout

With a digest2 executable and digest2.model.csv (and an Internet connection)
you should be able to run digest2 now.  The following sample observations are
provided as `sample.obs`.


```
     NE00030  C2004 09 16.15206 16 13 11.57 +20 52 23.7          21.1 Vd     291
     NE00030  C2004 09 16.15621 16 13 11.34 +20 52 16.8          20.8 Vd     291
     NE00030  C2004 09 16.16017 16 13 11.13 +20 52 09.6          20.7 Vd     291
     NE00199  C2007 02 09.24234 06 08 06.06 +43 13 26.2          20.1  c     704
     NE00199  C2007 02 09.25415 06 08 05.51 +43 13 01.7          20.1  c     704
     NE00199  C2007 02 09.26683 06 08 04.80 +43 12 37.5          19.9  c     704
     NE00269  C2003 01 06.51893 12 40 50.09 +18 27 46.9          21.4 Vd     291
     NE00269  C2003 01 06.52850 12 40 50.71 +18 27 46.1          21.8 Vd     291
     NE00269  C2003 01 06.54359 12 40 51.68 +18 27 42.5          21.9 Vd     291
```

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
otherwise get a copy of the Minor Planet Center's `obscode.dat` file and place
it in the current directory with the file name `digest2.obscodes`.

## Installation and configuration

See file OPERATION.md.

