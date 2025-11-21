# Digest2 operation, including installation and configuration
Digest2 version 0.19.3

## Basic operation

Having built digest2 (see [BUILDING.md](BUILDING.md), you should have a `digest2` executable in the current directory.
Make sure that you also have the `digest2.model.csv`, `digest2.model`, and `MPC.config` files in the current directory.
If you have internet connection `digest2` will download the latest observatory parallax data from the Minor Planet Center.
If no internet connection is available, you will need to download the `obscode.dat` file from the Minor Planet Center and 
place it in the current directory with the name `digest2.obscodes`.

You should now be able to run digest2. For this, we have provided two sample files: one in MPC format (`sample.obs`), and one 
in ADES format (`sample.xml`). More information on the MPC and ADES formats can be found in the 
[MPC documentation](https://minorplanetcenter.net/iau/info/MPOrbitFormat.html) and the
[ADES documentation](https://minorplanetcenter.net/iau/info/ADES.html), respectively.

For illustration purposes, we will use the MPC format file (`sample.obs`).

``` bash
K16S99K 1C2022 12 25.38496508 32 36.283+17 10 35.94         21.98GV     G96
K16S99K 1C2022 12 25.39527308 32 35.635+17 10 37.27         21.72GV     G96
K16S99K 1C2022 12 25.40040208 32 35.473+17 10 37.38         21.31GV     G96
```

Regardless of the format, digest2 is run the same way:

``` bash
digest2 <file_name>
```

Replace `<file_name>` with the name of the file you want to run digest2 on. For example, to run digest2 on `sample.obs`:

```bash 
digest2 sample.obs
```

Running the above should produce the following output:

``` bash
Desig.    RMS  RMS' Raw NID Raw NID Raw NID Raw NID Other Possibilities
K16S99K  0.73  0.00   0   0   9  14   3   6   1   1 (MC 13) (MB1 72) (MB2 <1) (JFC <1)
```

The RMS column provides the root-mean-square (`RMS`) value of residuals resulting from linear motion along a great circle.
A high RMS could indicate either inaccurate observations or a significant deviation from the great circle over the observation 
arc.
Therefore, it serves as a quick check to ensure the meaningfulness of scores.
If the `RMS` value is low, the scores are considered meaningful.
Even if the `RMS` is high due to great circle deviation, the scores still hold meaning.
However, `digest2` cannot differentiate between cases where the high `RMS` is caused by great circle departure or poor observations.

There is an optional keyword `rmsPrime`. When used, the output will have a column with the header `RMS'`. rmsPrime denotes the RMS computed from 
the user-submitted astrometric uncertainties in ADES input file. Comparison of RMS and RMSPrime gives potential hints for in-tracklet curvature,
 if the great-circle RMS is much larger then rmsPrime. The positive curvature is likely for nearby objects and only if the user-submitted
  uncertainties are reasonable. False-positive curvature is likely when the uncertainties are severly underestimated.
  If uncertainties are not provided, `RMS'` is zero.

The `Int`, `NEO`, `N22`, and `N18` columns display the `digest2` scores for different orbit classes (a complete list of orbit classes is provided 
at the bottom of this document): MPC Interesting, Near Earth Object (NEO), NEOs with an absolute magnitude (H) of 22 or less, and NEOs of H 18 or less,
respectively.
Orbit classes are determined based on orbital elements and can be either well-known dynamic populations like Hungarias (Hun) or popular classifications
like NEO.
A `digest2` score ranges from `0` to `100`, similar to a percentage. 
A score of `0` implies a minimal chance of the object belonging to the indicated orbit class, while a score of `100` indicates a high certainty
of the object being in the indicated class. However, the score is not an exact probability due to various factors.

The result above shows the higest score for the MB1 (inner main belt) orbit category. `RMS'` is zero because there aren't any uncertainties provided.

## Moving the executable

The digest2 executable built in BUILDING.md can be moved or copied
to a more convenient location such as a `bin` directory on your PATH.
It still needs to find the model file and obscodes file though, and by default
it simply looks in the current directory for these files. The command line
option `-p <path>` specifies an alternate directory.  One fairly simple
installation techique then is

1.  Move `digest2` to a directory on your PATH.
2.  Move `digest2.model.csv` to any convenient directory.
3.  Create a shell alias digest2=digest2 -p <model dir>.

## Command line options

Invoking digest2 without command line arguments (or with invalid arguments)
shows this usage prompt.

``` bash
Usage: digest2 [options] <obs file>    score observations in file
       digest2 [options] -             score observations from stdin
       digest2 -m <binary model file>  generate binary model from CSV
       digest2 -h or --help            display help and quick reference
       digest2 -v or --version         display program version and model date

Options:
       -c or --config <config file>
       -m or --model <binary model file>
       -o or --obscodes <obscode file>
       -p or --config-path <path>
       -u or --cpu <n-cores>
```

The help information lists a quick reference to keywords and orbit classes
allowed in the configuration file.  The configuration file is explained
below in the section digest2.config.

The options config, model, obscodes and config-path are described in the
next section.

The cpu option allows you to specify the number of operating system threads to
use.  The default is the number returned by the C function sysconf, typically
the total number of cores in the computer.

When digest2 first runs, it may create two additional files, `digest2.obscodes`
and `digest2.model`.  If the file `digest2.obscodes` is not present (and the
--obscodes command line option is not used) digest2 will attempt to create this
file by downloading obscode data from the MPC web site.

Also, the downloaded model file is in CSV format, but digest2
converts this to a binary form for faster loading on subsequent runs.  This
file is `digest2.model` (without the .csv) and is created if found to be
missing or out of date compared to the csv file.  These two files,
`digest2.obscodes` and `digest2.model` are not normally created 
Digest2 downloads
observatory code data only if finds it missing.  Similarly it writes a new
binary model file only if the csv file is updated.

## File formats

Input observations must either be in [MPC 80 column format](https://minorplanetcenter.net/iau/info/MPOrbitFormat.html)
or on [ADES format](https://minorplanetcenter.net/iau/info/ADES.html), supplied as either an .obs or .xml file.
Regardless, the observations should be sorted first by designation and then by time
of observation, and there should be at least two observations of each object.

The xml ADES input must start with `<?xml` and the file extension must be .xml
Other type of suffix or non-suffix input files are treated as MPC80 column format.

`digest2.obscodes` is a text file containing observatory codes in MPC format
used [here](http://www.minorplanetcenter.net/iau/lists/ObsCodes.html).

`digest2.model.csv` is a comma separated text file containing the Solar System
model used by `digest2`.

`digest2.model` is a binary encoding of `digest2.model.csv`. This file is created
by executing `./digest -c digest2.model.csv`

`digest2.config`, the optional configuration file, is a text file with a simple
format. Empty lines and lines beginning with # are ignored.  Other lines must
contain either a keyword or an orbit class.

`MPC.config` is provided as a list of the observational error allowances
currently used by the MPC.

## Configuring file locations

As described above the -p command line option is useful to specify a
directory for digest2 associated files, `digest2.config`, `digest2.obscodes`,
`digest2.model`, and `digest2.model.csv`.

For greater control, file locations can be specified individually:

``` bash
File               Command line option
digest2.obscodes   -o
digest2.model      -m
digest2.config     -c
``` 

A configuration file is required to be present if -c is used.

If you specify -p in combination with -c, -o, or -m, the path specified
with the -c, -o, or -m option takes precedence.  That is, the path specified
with -p is not joined with a file name specified with -c, -o, or -m.

The -o and -m options can also be used in a form of the digest2 command without
input observations.  With -o, the action is to get a fresh copy of obscode data
from the MPC website and store it to the specified file.  With -m, the action
is to read `digest2.model.csv` and write the binary form to the specified
file.

## digest2.config

Allowable keywords:

``` bash
headings
noheadings
rms
rmsPrime
norms
raw
noid
repeatable
random
obserr
poss
noThreshold
```


The `headings` and the `rms` columns can be turned off if desired by simply removing the keyword from the configuration file.

Keywords `raw` and `noid` determine the score produced as described in [ALGORITHM.md](ALGORITHM.md).  
The default is `noid`.  If both keywords are present, both scores are output.

Keyword `rms` returns great-circle RMS of the tracklet, if there are more than 2 detections per tracklet.

Keyword `rmsPrime` returns the RMS from the user-submitted uncertainties in ADES (XML) format.

Keyword `noThreshold` is an optional keyword that allows user to accept reported astrometric uncertainties as-is. 
The default functionality of digest2 sets floor and ceiling for the ADES-provided uncertainties. If the uncertainty
is less than the floor, it is set to floor; if it is larger than the ceiling, it is set to the ceiling value.
The floor and the ceiling values are set to 0.7 and 5-times the mean (expected) uncertainty for the observatory
code as it is provided in the configuration file. If the observary is not present in the configuration file,
default value of 1.0" is used. Thresholds are used by default to avoid severly underestimated or overestimated
uncertainty values that would affect the resulting digest2 score as well as the `RMS'`. However, in case
the reported uncertainties are trusted, one could use the `noThreshold` keyword that would accept user-supplied
astrometric uncertainties.

The keywords `repeatable` and `random` determine if program output is
strictly repeatable or can be non-deterministic from one run to the next, for which `digest2` uses a Monte Carlo method.  
By default, the pseudo random number generator is seeded randomly. 
When the keyword `repeatable` is used, it is reseeded with a constant value for each tracklet, yielding repeatable scores.

Keyword `obserr` specifies the amount of observational error that the algorithm should allow for.  
It is specified in arc seconds as in,

``` bash
obserr = 0.7
```

The default, if no `obserr` is specified, is `1.0` arc seconds.
`Obserr` may be specified for individual observatory codes as in,

``` bash
obserrF51 =.3
obserr704 = 1
```

The keyword `poss` pertains to output the "Other Possibilities" column.
By default, other possibilities are suppressed if orbit classes are
explicitly specified.

Listing an orbit class limits scoring to only the listed classes.
Other possibilities are not computed or listed. Either abbreviations or
long forms may be used. In any case they must be spelled exactly as
shown.

Example 1:

``` bash
Int
Neo
N22
N18
poss
```

This is equivalent to default program behavior without a config file.

Example 2:

``` bash
# just three
NEO
Hun
JTr
```

The program output is:

```bash
Desig.    RMS NEO Hun JTr
NE00030  0.15 100   0   0
NE00199  0.56  97   0   0
NE00269  0.42  18   4   0
```

The program runs considerably faster in this case, as it computes scores for
only these three classes and not all possible classes.

Example 3:

```bash
noheadings
norms
N22
```

output:

``` bash
NE00030  37
NE00199  18
NE00269   3
```

This might be useful for generating results to be analyzed by another program.

Example 4:

Run `digest2 -c MPC.config sample.obs`.

output:

``` bash
Desig.    RMS Int NEO N22 N18 Other Possibilities
NE00030  0.15 100 100  36   0
NE00199  0.56  98  98  17   0 (MC 2) (JFC 1)
NE00269  0.42  24  23   4   0 (MC 7) (Hun 3) (Pho 15) (MB1 <1) (Han <1) (MB2 41) (MB3 5) (JFC 1)
```

The command line option `-c` specifies to use `MPC.config` as the config file.
This file specifies `obserr` for selected observatories.  Included is code 291,
the observing site for objects NE00030 and NE00269. Notice Int and NEO scores
on NE00269 in particular are somewhat higher than before. The `obserr` settings
can sometimes significantly affect scores. If you are interested in emulating
scores obtained internally at the MPC, you should use `obserr` settings from
this file.

Example 5:

Input provided in a form of standard input (stdin).

Run `cat sample.obs|./digest2 -`

or

Run `cat sample.xml|./digest2 - -c MPC.config`

Note that the dash is used instead of the filename.


## Currently supported orbit classes:

``` bash
Abbr.  Long Form
---    -------------
Int    MPC interest.
NEO    NEO(q < 1.3)
N22    NEO(H <= 22)
N18    NEO(H <= 18)
MC     Mars Crosser
Hun    Hungaria gr.
Pho    Phocaea group
MB1    Inner MB
Pal    Pallas group
Han    Hansa group
MB2    Middle MB
MB3    Outer MB
Hil    Hilda group
JTr    Jupiter tr.
JFC    Jupiter Comet
```
