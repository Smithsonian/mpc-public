# 223

223.f is the oldest known version of digest2, the file as given to me
by Tim Spahr.

## Found

On CF machine byron.  The file contains copyrighted code and should not be
placed on a public repository.

## Build

If you have an old enough f77,

    f77 223.f

On a more modern computer,

    gfortran -std=legacy 223.f

## Run

Required files are the 9001 line `AST.BIAS.POP` and the files `ET` and
`OBSERVATORY` from the src dir.

This AST.BIAS.POP goes to 25 AU and 223.f reads all of it.  For later
versions of digest2 I truncated this at 6 AU.

OBSERVATORY is a file of site parallax constants similar to obscode.dat.
The constants are in a different format.
Also 223.f reads codes as I3 and so handles only fully numeric 3 digit codes.

Example run,

```
$ ./a.out 
 INPUTFILE (J2000 OBSERVATIONS)
../data/README-01.obs
   #        Design    Score   NEO?   Elong  Elat  ElongR   ElatR  TotalR   Mag
   1        C5O0011    37.2   NEO   -174.8   8.7  -0.315   0.056   0.320  19.4
```

A quirk of this version is that the data file should have a trailing blank
line.  Without it the last object is dropped.

A few files are left behind, `PANGLO.EMP`, `PANGLO.MPC`, `digest.hold`, and
`test8.out`.  These can be ignored.
