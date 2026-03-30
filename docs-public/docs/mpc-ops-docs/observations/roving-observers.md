# "Roving Observer" Extensions

The use of observatory codes to indicate the site of observation is intended for rarely/infrequently-visited or occasional (expedition-style) non-permanent sites. In recognition of
the fact that there may be circumstances under which a telescope is
transported to a temporary site for some reason for the purpose of performing
minor-body astrometry and recognizing that assigning this one-time site an
observing code would not be worthwhile, the MPC observation format has been
extended to allow observations made at such sites to be published. Please do not submit your astrometry as a roving observer from a permanent location/telescope -- instead apply for an [observatory code](../astrometry/observatory-codes.md#how-do-i-get-an-observatory-code)
if you intend a regular use of the site/telescope for submission of your astrometry.

All "roving observer" observations are represented by a single observatory
code: **247**. Each "roving observer" observation consists of two 80-column
records. The 247 observatory code appears on both records. The first
80-column record is otherwise identical to the [format for
optical observations](mpc1992-format.md#optical-observations), with one minor change: column 15 contains "V". The format of the second 80-column record
is described below. 

Note that in 2021, a new roving observatory code (**270**) was created and assigned for the sole use of the Unistellar network, using the same two-line format as for the observatory code 247.

---

## Summary of 2nd-Record Format

Please note that TABs must NOT be used. Columns marked as 'blank'
must contain spaces (ASCII 32). The format is identical for both comets
and minor planets.

```
   Columns          Use
    1 - 12          Identical to columns 1-12 of first record
   13        A1     Blank
   14               Identical to column 14 of first record
   15        A1     'v'
   16 - 32          Identical to columns 16-32 of first record
   33        A1     '1'
   34        A1     Blank
   35 - 44   F10.6  E longitude of observing site (to an
                       appropriate number of d.p., generally to
                       4 d.p.).  Decimal point in column 38.
   45        A1     Blank
   46 - 55   F10.6  Latitude (N +ve, S -ve) of observing site,
                       (to an appropriate number of d.p.,
                       generally to 4 d.p.).  Sign in column 46,
                       decimal point in column 49.
   56        A1     Blank
   57 - 61   I5     Altitude in meters (right justified, no
                       leading zeroes, e.g., '  690', not '690  '
                       or '00690')
   62 - 77   A      Blank
   78 - 80   A3     '247'
```

Longitudes and latitudes are geographic.
