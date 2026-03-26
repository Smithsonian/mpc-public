# Format for Astrometric Observations of Comets, Minor Planets and Natural Satellites

This page describes the MPC1992 80-column record format for submitting astrometric observations
of comets, minor planets and natural satellites for publication in the
[*Minor Planet Circulars (MPCs)*](https://minorplanetcenter.net/iau/services/MPCServices.html),
[*Minor Planet Electronic Circulars (MPECs)*](https://minorplanetcenter.net/iau/services/MPCServices.html)
and [*IAU Circulars*](https://minorplanetcenter.net/iau/services/IAUC.html).

---

## Observation Types

Three primary observation formats are documented:

- [Optical](#optical-observations) (photographic, CCD or visual)
    - ["Roving Observer" format](roving-observers.md)
- [Satellite-based](https://minorplanetcenter.net/iau/info/SatelliteObs.html)
- [Radar](https://minorplanetcenter.net/iau/info/RadarObs.html)

### Related Links

- [References](https://minorplanetcenter.net/iau/info/References.html)
- [Packed provisional designations](../designations/packed-designations.md)
    - [Packed designations for comets discovered/recovered in the past year](https://minorplanetcenter.net/iau/lists/LastYear.html)
- [Alphabetic notes for observations](https://minorplanetcenter.net/iau/info/ObsNote.html)
- [Observatory codes](https://minorplanetcenter.net/iau/lists/ObsCodesF.html)
- You should also ensure that you have read the [Guide to Minor-Body Astrometry](../astrometry/index.md)

Observations formatted according to the schemes detailed above must
be sent via e-mail to [`obs@cfa.harvard.edu`](mailto:obs@cfa.harvard.edu).
Observations must be sent unencoded as plain text. In particular, users
of MIME-compliant mailers are asked **not** to use BinHex/Base64
encoding! Encoded messages are not decoded by the automated processing
routines (a deliberate design decision), so any encoded observation batches
will not be recognized as containing observations and will be deleted.

---

## Optical Observations

### Summary of Format

Please note that TABs must NOT be used. Columns marked as 'blank'
must contain spaces (ASCII 32). The Fortran formats listed below are
for writing purposes.

#### Minor Planets (Columns 1-13)

```
   Columns     Format   Use
    1 -  5       A5     Packed minor planet number
    6 - 12       A7     Packed provisional designation, or a temporary designation
   13            A1     Discovery asterisk
```

Minor planet numbers and [provisional designations](../designations/packed-designations.md) are official designations
assigned by the Minor Planet Center. Temporary designations are designations,
preferably no more than six (6) characters long (the absolute maximum is
seven (7) characters), assigned by the observer for new or
unidentified objects. Temporary designations must consist of alphanumeric
characters only; do not include spaces. All observations of the same "new"
object reported in the same message must have the same temporary designation.

#### Comets

```
   Columns     Format   Use
    1 -  4       I4     Periodic comet number
    5            A1     Letter indicating type of orbit
    6 - 12       A7     Provisional or temporary designation
   13            X      Not used, must be blank
```

Periodic comet numbers and [provisional designations](../designations/packed-designations.md) are official designations
assigned by, respectively, the Minor Planet Center and Central Bureau for
Astronomical Telegrams. Temporary designations are designations,
up to six (6) characters long, assigned by the observer for new or
unidentified objects. In practice, temporary designations on comet
observations will be very rare.

#### Natural Satellites

```
   Columns     Format   Use
    1            A1     Planet identifier [Only if numbered]
    2 -  4       I3     Satellite number  [Only if numbered]
    5            A1     "S"
    6 - 12       A7     Provisional or temporary designation [Only if not numbered]
   13            X      Not used, must be blank
```

#### Minor Planets, Comets and Natural Satellites

```
   Columns     Format   Use
   14            A1     Note 1
   15            A1     Note 2
   16 - 32              Date of observation
   33 - 44              Observed RA (J2000.0)
   45 - 56              Observed Decl. (J2000.0)
   57 - 65       9X     Must be blank
   66 - 71    F5.2,A1   Observed magnitude and band
                           (or nuclear/total flag for comets)
   72 - 77       X      Must be blank
   78 - 80       A3     Observatory code
```

---

### Detailed Notes

#### Minor Planets

**Number**
: Columns 1-5 contain a zero-padded, right-justified number -- e.g., an
observation of [(1)](https://data.minorplanetcenter.net/explorer/?tab=Designated&search=1) would be given as `00001`, an observation of [(3202)](https://data.minorplanetcenter.net/explorer/?tab=Designated&search=3202) would
be `03202`. If there is no number, these columns must be blank. Six-digit
numbers are to be stored in packed form (`A0000 == 100000`), in order to
be consistent with the format specifier earlier in this document.

**Provisional/Temporary Designation**
: Columns 6-12 contain the provisional designation or the temporary
designation. The provisional designation is stored in a
[7-character packed form](../designations/packed-designations.md).

!!! note
    Temporary designations are designations assigned by the observer for new
    or unidentified objects. Such designations must begin in column 6,
    should not exceed 6 characters in length, and should start with one or more
    letters.

    It is important that every observation has a designation and that the
    same designation is used for all observations of the same object.

**Discovery Asterisk**
: Discovery observations for new (or unidentified) objects should contain
`*` in column 13. Only one asterisked observation per object is
expected. Some objects consist of multiple designations, in that case each
designation keeps its original discovery asterisk.

#### Comets

**Periodic Comet Number**
: Periodic comets that have been observed at more than one return are
assigned numbers. Reference should be made to the editorial notices
on [*MPC* 23803-23804](https://minorplanetcenter.net/iau/ECS/MPCArchive/1994/MPC_19940828.pdf) and [24421](https://minorplanetcenter.net/iau/ECS/MPCArchive/1995/MPC_19950116.pdf) for more complete details of the
circumstances under which numbers are assigned.

    Examples:

    ```
      Comet                  P/ Number    Columns 1-4
                                          will contain
      P/Halley                  1P          0001
      P/Encke                   2P          0002
      P/Biela                   3D          0003
      P/Wild 4                116P          0116
    ```

    See the complete list of [periodic comet numbers](https://minorplanetcenter.net/iau/lists/PeriodicCodes.html).

**Orbit Type**
: Column 5 contains `C` for a long-period comet, `P` for a short-period
comet, `D` for a 'defunct' comet, `X` for an uncertain comet, `I` for an interstellar object, or `A` for a
minor planet given a cometary designation or objects suspected to be comets.

**Provisional Designation**
: Columns 6-12 contain a packed version of the provisional designation.
The first two digits of the year are packed into a single character
in column 6 (where `I == 18`, `J == 19`, `K == 20`). Columns 7-8 contain the last
two digits of the year. Column 9 contains the half-month letter.
Columns 10-11 contain the order within the half-month. Column 12 will
be normally be `0`, except for split comets, when the fragment designation
is stored there as a lower-case letter.

    ```
   Examples:
   1995 A1   = J95A010
   1994 P1-B = J94P01b   refers to fragment B of 1994 P1
   1994 P1   = J94P010   refers to the whole comet 1994 P1
    ```

Columns 6-12 may contain a minor planet provisional designation. In such situations, column 12 will contain a capital letter.

#### Natural Satellites

**Planet Identifier**
: A single character to represent the planet that the satellite belongs to.

    ```
   Char   Planet
     J    Jupiter
     S    Saturn
     U    Uranus
     N    Neptune
    ```

    This is given in column 1 for those objects with Roman numeral designations and column 9 for those with provisional designations.

**Satellite Number**
: For those objects with Roman numeral designations, columns 2-4 contain
the number of the satellite.

**Column 5**
: Column 5 is always `S` for a satellite observation.

**Provisional Designation**
: Columns 6-12 contain a packed version of the provisional designation
for those objects without Roman numeral designations.

    The first two digits of the year are packed into a single character
    in column 6 (I = 18, J = 19, K = 20). Columns 7-8 contain the last
    two digits of the year.
    Columns 10-11 contain the order within the year. Column 12 will
    be always be `0`. This is similar to the scheme used for comets.

    ```
   Examples
   123456789012
   J013S         Jupiter XIII
   N002S         Neptune II
       SJ99U030  S/1999 U 3    (Third new Uranian satellite discovered in 1999)
       SK20J010  S/2020 J 1    (First new Jovian satellite discovered in 2020)
    ```

#### Comets, Minor Planets and Natural Satellites

**Note 1**
: This column contains an alphabetical publishable note or (those sites that
use program codes) an alphanumeric or
non-alphanumeric character program code. The list of [standard codes](https://minorplanetcenter.net/iau/info/ObsNote.html) used
for observations of minor planets is given in each batch of
[*MPCs*](https://minorplanetcenter.net/iau/services/MPCServices.html).

**Note 2**
: This column serves two purposes. For those observations which have been
converted to the J2000.0 system by rotating B1950.0 coordinates, this column
contains `A`, to indicate that the value has been adjusted. For those
observations reduced in the J2000.0 system this column is used to indicate
how the observation was made. The following codes will be used:

    ```
      P   Photographic
      e   Encoder
      C   CCD
      B   CMOS
      T   Meridian or transit circle
      M   Micrometer
     V/v  "Roving Observer" observation
     R/r  Radar observation
     S/s  Satellite observation
      c   Corrected-without-republication CCD observation [MUST NOT be used on submissions]
      E   Occultation-derived observations
      O   Offset observations (used only for observations of natural satellites)
      H   Hipparcos geocentric observations
      N   Normal place
      n   Mini-normal place derived from averaging observations from video frames

      D   CCD observation converted from original XML-formatted submission [MUST NOT be used on submissions]
      Z   Photographic observation converted from original XML-formatted submission [MUST NOT be used on submissions]
     W/w  "Roving observer" observation converted from original XML-formatted submission [MUST NOT be used on submissions]
     Q/q  Radar observation converted from original XML-formatted submission [MUST NOT be used on submissions]
     T/t  Satellite observation converted from original XML-formatted submission [MUST NOT be used on submissions]
    ```

    In addition, there are `X` and `x` which are used only for already-filed observations.
    `X` was given originally only to discovery observations that were approximate or
    semi-accurate and that had accurate measures corresponding to the time
    of discovery: this has been extended to other replaced discovery observations.
    Observations marked `X`/`x` are to be suppressed in residual blocks.
    They are retained so that there exists an original record of a discovery.
    These codes MUST NOT be used on observation submissions.

**Date of Observation**
: Columns 16-32 contain the date and UTC time, usually corresponding to the
mid-point of observation. If the astrometry refers to one end of a trailed image,
then the time of observation should be either the start time of the exposure or the finish
time of the exposure, depending on which end of the trail was measured.
The format is `YYYY MM DD.dddddd`, with the decimal day of observation normally being given to a precision of 0.00001
days. *Where such precision is justified*, there is the option of recording times to 0.000001 days.

**Observed RA (J2000.0)**
: Columns 33-44 contain the observed J2000.0 right ascension. The format
is `HH MM SS.ddd`, with the seconds of R.A. normally being given to a
precision of 0.01s. There is the option of
recording the right ascension to 0.001s, *where such precision is
justified*.

**Observed Decl (J2000.0)**
: Columns 45-56 contain the observed J2000.0 declination. The format is
`sDD MM SS.dd` (with `s` being the sign), with the seconds of Decl.
normally being given to a precision of 0.1". There is the option of
recording the declination to 0".01, *where such precision is justified*.

**Observed Magnitude and Band**
: The observed magnitude (normally to a precision of 0.1 mag.) and the band
in which the measurement was made. The observed magnitude can
be given to 0.01 mag., *where such precision is justified*. The default
magnitude scale is photographic, although magnitudes may
be given in V- or R-band, for example. In the past for comets, the magnitude
was specified as being nuclear, N, or total, T, but observers are now encouraged to
provide the actual band used.

    The current list of acceptable magnitude bands is: B, V, R, I, J, W, U, C, L, H, K, Y, G, g, r, i, w, y, z, o, c, v, u. Non-recognized
    magnitude bands will
    cause observations to be rejected. Addition of new recognised bands
    requires knowledge of a standard correction to convert a magnitude in that
    band to V. Conversion to V band used by MPC is located [here](https://minorplanetcenter.net/iau/info/BandConversion.txt).

    The formerly-used "C" band to indicate "clear" or "no filter"
    is no longer valid for newly-submitted observations, but will remain on
    previously-submitted observations.

**Observatory Code**
: Observatory codes are stored in columns 78-80.
Lists of [observatory codes](https://minorplanetcenter.net/iau/lists/ObsCodes.html) are
published from time to time in the [*MPCs*](https://minorplanetcenter.net/iau/services/MPCServices.html).
Note that new observatory codes are assigned only upon receipt of
acceptable astrometric observations.
