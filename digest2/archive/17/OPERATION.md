# Digest2 operation, including installation and configuration
Digest2 version 0.19

## Basic operation

"Initial program checkout" in BUILDING.md used this example data,

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

in file `sample.obs` and showed the command `digest2 sample.obs` producing this
output:

```
NE00030  0.15 100 100  37   0
NE00199  0.56  98  97  17   0 (MC 2) (JFC 1)
NE00269  0.42  18  18   3   0 (MC 9) (Hun 4) (Pho 27) (MB1 <1) (Han <1) (MB2 30) (MB3 12) (JFC 1)
```

The column RMS gives the residual RMS from linear motion along a great circle.
The columns Int, NEO, N22, and N18 are showing the digest2 scores in various
orbit classes, MPC Interesting, Near Earth Object, NEOs with absolute magnitude
(H) of 22 or less, and NEOs of H 18 or less.

A digest2 score ranges from 0 to 100 like a percentage chance.  A score of
0 means almost no chance of the object being of the indicated orbit class,
a score of 100 means almost certainty that the object is of the indicated
class.  For various reasons the score is not an exact probability.

In this example digest2 predicts that the first two objects are almost certain
to be NEOs.  The last one, with a NEO score of only 18 shows little chance of
being a NEO.  The results Pho 27, MB2 30, and MB3 12 show that it is much more
likely to have a Phocaea-like or main belt orbit.

Orbit classes are based on orbital elements and are either known dynamic
populations like Hungarias (Hun) or popular classifications like NEO.  The
complete list is given below.

The RMS figure is a root-mean-square of residuals in arc seconds of the
observations against a great circle fit.  A high RMS could indicate either bad
observations or significant great circle departure over the observation arc.
It can thus be used as a quick check that scores are meaningful.  If the RMS
is low, scores are meaningful.  Scores are still meaningful if the RMS is high
due to great circle departure, but digest2 offers no way of distinguishing this
case from one where observations are bad.

Further instructions in this file cover moving the digest2 executable to a
more convenient location, configuration, and command line operation.

## Moving the executable

The digest2 executable built in BUILDING.md can be moved or copied
to a more convenient location such as a `bin` directory on your PATH.
It still needs to find the model file and obscodes file though, and by default
it simply looks in the current directory for these files.  The command line
option `-p <path>` specifies an alternate directory.  One fairly simple
installation techique then is

1.  Move `digest2` to a directory on your PATH.
2.  Move `digest2.model.csv` to any convenient directory.
3.  Create a shell alias digest2=digest2 -p <model dir>.

## Command line options

Invoking digest2 without command line arguments (or with invalid arguments)
shows this usage prompt.

```
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

Observations, whether supplied in a file or through stdin, should contain
observations in the MPC 80 column observation format, documented at
http://www.minorplanetcenter.net/iau/info/OpticalObs.html.
The observations should be sorted first by designation and then by time
of observation, and there should be at least two observations of each object.

digest2.obscodes is a text file containing observatory codes in MPC format
used at http://www.minorplanetcenter.net/iau/lists/ObsCodes.html.

digest2.model.csv is a comma separated text file containing the Solar System
model used by digest2.

digest2.model is a binary encoding of digest2.model.csv.

digest2.config, the optional configuration file, is a text file with a simple
format.  Empty lines and lines beginning with # are ignored.  Other lines must
contain either a keyword or an orbit class.

MPC.config is provided as a list of the observational error allowances
currently used by the MPC.  This file is included (along with
digest2.model.csv) in d2model.tar.bz2.  See BUILDING.md.
## Configuring file locations

As described above the -p command line option is useful to specify a
directory for digest2 associated files, `digest2.config`, `digest2.obscodes`,
`digest2.model`, and `digest2.model.csv`.

For greater control, file locations can be specified individually:

	File               Command line option
	digest2.obscodes   -o
	digest2.model      -m
	digest2.config     -c

A configuration file is required to be present if -c is used.

If you specify -p in combination with -c, -o, or -m, the path specified
with the -c, -o, or -m option takes precedence.  That is, the path specified
with -p is not joined with with a file name specified with -c, -o, or -m.

The -o and -m options can also be used in a form of the digest2 command without
input observations.  With -o, the action is to get a fresh copy of obscode data
from the MPC web site and store it to the specified file.  With -m, the action
is to read `digest2.model.csv` and write the binary form to the specified
file.

## digest2.config

Allowable keywords:

    headings
    noheadings
    rms
    norms
    raw
    noid
    repeatable
    random
    obserr
    poss

Headings and the rms column can be turned off if desired.

Keywords raw and noid determine the score produced as described in the
document ALGORITHM.md.  The default is noid.  If both keywords are present,
both scores are output.

The keywords repeatable and random determine if program output is
strictly repeatable or can be non-deterministic from one run to the next.
The program uses a Monte Carlo method.  By default, the pseudo random
number generator is seeded randomly.  When the keyword repeatable is
used, it is reseeded with a constant value for each tracklet, yielding
repeatable scores.

Keyword obserr specifies the amount of observational error that the algorithm
should allow for.  It is specified in arc seconds as in,

```
obserr=0.7
```

The default, if no obserr is specified, is 1.0 arc seconds.
Obserr may be specified for individual observatory codes as in,

```
obserrF51=.3
obserr 704 = 1
```

As shown, white space is optional.

The keyword poss specifies to output the "Other Possibilities" column.
By default, other possibilities are suppressed if orbit classes are
explicitly specified.

Orbit classes:

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

Listing an orbit class limits scoring to only the listed classes.
Other possibilities are not computed or listed.  Either abbreviations or
long forms may be used.  In any case they must be spelled exactly as
shown.

Example 1:

```
Int
Neo
N22
N18
poss
```

This is equivalent to default program behavior without a config file.

Example 2:

```
# just three
NEO
Hun
JTr
```

program output is

```
Desig.    RMS NEO Hun JTr
NE00030  0.15 100   0   0
NE00199  0.56  97   0   0
NE00269  0.42  18   4   0
```

The program runs considerably faster in this case, as it computes scores for
only these three classes and not all possible classes.

Example 3:

```
noheadings
norms
N22
```

output:

```
NE00030  37
NE00199  18
NE00269   3
```

This might be useful for generating results to be analyzed by another program.

Example 4:

Run `digest2 -c MPC.config sample.obs`.

output:

```
Desig.    RMS Int NEO N22 N18 Other Possibilities
NE00030  0.15 100 100  36   0
NE00199  0.56  98  98  17   0 (MC 2) (JFC 1)
NE00269  0.42  24  23   4   0 (MC 7) (Hun 3) (Pho 15) (MB1 <1) (Han <1) (MB2 41) (MB3 5) (JFC 1)
```

The command line option -c specifies to use MPC.config as the config file.
This file specifies obserr for selected observatories.  Included is code 291,
the observing site for objects NE00030 and NE00269.  Notice Int and NEO scores
on NE00269 in particular are somewhat higher than before.  The obserr settings
can sometimes significantly affect scores.  If you are interested in emulating
scores obtained internally at the MPC, you should use obserr settings from
this file.
