#digest 2, population directory

last updated: July 14, 2023

The population directory contains:

1) archive dir. with previous versions of the files

2) MPC.config - list of 140 observatory codes with mean
(expected) astrometric uncertainties and a few config.
keywords

3) digest2.model.csv - binned population model with full
solar system (SSM) and undiscovered part (full minus the
known catalog from 2023). user must create digest.model binary
file as an input for digest2 by running
`./digest2 -m digest2.model `  (name of the binary can be user-
defined)

4) digest2.model - compiled binary

5) digest2.obscodes - MPC observatory codes as in 2023:
current can be downloaded from
https://minorplanetcenter.net//iau/lists/ObsCodes.html)

6) make_population directory with muk and s3m code that can
create a binned population model csv (needs SSM files from
Grav et al, 2011. The Pan-STARRS Synthetic Solar System Model:
A Tool for Testing and Efficiency Determination of the Moving
Object Processing System. PASP 123, No. 902.
