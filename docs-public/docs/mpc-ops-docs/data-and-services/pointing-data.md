# Pointing Data

This page gives details on how to access the raw pointing files that are used to prepare the Sky Coverage plots. The raw pointing files are released only when the observers give permission to do so.

Further details on the Sky Coverage plots and the underlying data can be found on the 
[Sky Coverage Submission page](https://minorplanetcenter.net/iau/info/Coverage.html) and 
[Sky Coverage Plots](https://www.minorplanetcenter.net/iau/SkyCoverage.html) pages.

The complete data files are available as a gzip'ed tar file [here](https://minorplanetcenter.net/iau/data/skycov.tgz) (N.B. this tar file is large).

If observers notice that data files are not available for a particular date, the data can simply be [resubmitted](https://minorplanetcenter.net/iau/info/Coverage.html).

## File Layout

The data files are arranged by year (the directory name being the four-digit year). Individual data files are named:

```
<OBSERVER>_<YEAR><DAYOFYEAR>.txt
```

where OBSERVER is a code representing the observer (it might be an observatory code or a survey name), YEAR is the year of observation and DAYOFYEAR is the day number within YEAR.

Within each file, each frame is represented on a single line, with four R.A./Decl. pairs (each in radians, representing the four corners of the observed field) and a limiting magnitude (which may be omitted).

Periodically, ZIP files are created containing all files from a particular year.

## Notes

- OBSERVER is set by the observer. Some observers are inconsistent in the name they use.
- The files are as processed by the SkyCov procedure. If certain information is not in these files, then it was not reported to the MPC and we do not have it.
- Some observers do not indicate limiting magnitude on a frame-by-frame basis, but simply give a fixed value. If we are informed that this is the case for a particular OBSERVER in the list below, the name is marked with an asterisk.

## Available Observers

Data files for the following OBSERVERs are currently available (three character OBSERVER codes are the observatory codes):

- SPACEWATCH (\*)
- 691 (\*)
- 683
- 333
- CATALINA
- CSS
- E12
- G96
- 924
- 699
- 608
- 644
- NEAT
- LINEAR
- 428
