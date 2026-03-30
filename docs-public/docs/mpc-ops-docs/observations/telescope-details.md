# Specifying Telescope Details in the Observational Header

It is important that information supplied by observers in the observational
headers accompanying each batch of observations be checked for validity
before the information is published in the *MPCs* or the *MPECs*.
Unverified material should not be permitted into either journal.
Due to the volume of incoming observational material, it is impractical
to inspect manually all incoming batches for compliance of header material
with the requirements listed on these pages. Such verification must be handled
entirely automatically. To this end, it is necessary for observers to
follow broad guidelines when supplying information with all the keywords in
the observational header. Historically, the most problems have come from the descriptions
of the telescopes (specified using the `TEL` keyword).

This document describes how to format the information contained on the
`TEL` line so that the automatic processing code can make sense of it.

- [Go straight to simple description](#the-simple-description) (sufficient for almost all observers).
- [Go straight to examples of valid simple TEL lines](#simple-examples).
- [Go straight to detailed description](#the-full-description).
- [Go straight to examples of valid detailed TEL lines](#detailed-examples).

---

## 1: The TEL Line

A valid `TEL` line consists of an ASCII line containing `TEL ` in columns
1-4, followed by one or more telescope descriptors. A telescope descriptor
describes a single instrument, in a format consistent with the descriptions
below. If more than
one telescope descriptor is given on the same `TEL` line, the descriptors
must be separated by commas followed by a space.

```
TEL <descriptor>[, <descriptor>]...
```

where items enclosed in square brackets are optional, `...` indicates
possible multiple repeats of the preceding item, and characters not surrounded by `<>` are string
literals.

In the descriptions below `<real>` indicates a positive real number,
either integer or non-decimal: if the value is less than 1, a leading
zero must be given. Examples of valid values are "1", "3.44" and "0.76".
Also, `<int>` indicates a positive integer, and `|` indicates
a logical OR.


## 2: The Notification Process

As of 2004 August 2, the automated acknowledgement message includes
information on the success or otherwise of the processing code's understanding
of the `TEL` lines included in each submission.

This notification includes a list of each `TEL` line found in your
message, followed by the value extracted by the processing code.
Then follows one of three summary messages, informing you that:

- Your `TEL` lines are completely compliant with this document.
- Your `TEL` lines are not completely compliant with this
  document, but the processing code thinks it has corrected them.
- The processing code couldn't understand your `TEL` lines.

If you get the second or third summary message, you are pointed to the
[observational header documentation](observational-details.md), in the
hope that future `TEL` lines will be specified correctly.


## 3: The Correction Process

The processing code has the ability to fix malformed descriptors. It is
not possible to fix all malformed descriptors in an entirely automatic
fashion (and some are so malformed, it is even difficult to do the fix
manually!), but the processing code applies a series of rules to each
malformed descriptor it finds, trying to make the descriptor valid.

The complete rules by which the processing code attempts to fix incoming
headers will not be documented. Suffice to say, the code will cope with
many types of malformed descriptors. However, the notification procedure now
informs observers when their `TEL` lines require fixing, so observers
should make their `TEL` lines valid on future batches.

If you get back a message saying that the processing code could not understand
or changed what you believe to be a valid `TEL` line,
please [report this immediately](https://minorplanetcenter.net/iau/FeedBack.html). Be sure
to include the observational header (please do not include the observations).


## 4: The Simple Description

For most observers, the simple description of telescope descriptors given
below (it is also described [elsewhere](observational-details.md)) will
be sufficient:

```
<descriptor> = <aperture> [<f/ratio> ]<instype>[ + CCD][ +[ <f/ratio>] focal reducer]
```

where:

- `<aperture>` is the aperture of the instrument in meters:
  `<aperture> = <real>-m`. E.g.,
  "0.50-m" or "1.0-m". If the aperture is given to more than
  two decimal places, the value will be rounded to two decimal places.
- `<f/ratio>` is the focal ratio of the instrument or the
  focal reducer:
  `<f/ratio> = f/<real>`. E.g., f/6.7 or f/3.
  If the focal ratio is given to more than
  two decimal places, the value will be rounded to two decimal places.
- `<instype>` is the type of the instrument. Types have to match
  one of the [types listed below](#defined-types-of-instrument).

### Simple Examples

The following examples of `TEL` lines have been verified as
correct by the code that vets incoming observation batches:

```
TEL 0.30-m Schmidt-Cassegrain + CCD
TEL 0.6-m f/6 reflector + CCD
TEL 0.28-m f/4.3 reflector + CCD
TEL 0.41-m f/10 Schmidt-Cassegrain + CCD + f/6.3 focal reducer
TEL 0.15-m f/12 refractor
```


## 5: The Full Description

The full description of telescope descriptors is as follows:

```
<descriptor> = <aperture>[/<aperture>] [<f/ratio> ]<instype>[ +[ <CCDsize>][x<CCDsize>] CCD][ +[ <f/ratio>] focal reducer][ + <extra>]
```

where the items are as defined in the Simple Description, with the addition
of the following:

- `<CCDsize>` is the size in pixels along one dimension of the CCD.
  `<CCDsize> = <int>|<int>K`.
  Examples of valid values are "2048" and "8K".
  For a square CCD it is anticipated that only one value be given: e.g.,
  "1024". For rectangular CCDs, the sizes in both dimensions should be given:
  e.g., "8Kx1K".
- `<extra>` is an "extra", taken from the
  list of [allowable extras listed below](#defined-extras).

### Detailed Examples

The following examples of `TEL` lines have been verified as
correct by the code that vets incoming observation batches:

```
TEL 2.2-m University of Hawaii reflector + 8K CCD
TEL 0.5-m/0.8-m Schmidt + CCD
TEL 3.58-m New Technology Telescope + EMMI-RILD system
```


## 6: Defined Types of Instrument

The list of defined instrument types is as follows:

```
Ritchey-Chretien         Schmidt-Cassegrain       Schmidt
Newtonian reflector      Cassegrain reflector     Cassegrain
hyperbolic astrograph    double astrograph        visual astrograph
astrograph               reflector                refractor
Deltagraph               Hypergraph               Maksutov-Newtonian
Maksutov-Cassegrain      Maksutov                 Schmidt-Newtonian
Coude                    Corrected Dall-Kirkham   Riccardi-Honders
```

Requests to allow further instrument types will be entertained.

In addition, there are a number of named professional instruments that
are permitted:

```
University of Hawaii reflector          Spacewatch telescope
KLENOT Telescope                        Canada-France-Hawaii Telescope
New Technology Telescope                Danish Telescope
Nordic Optical Telescope                Keck IV
Keck III                                Keck II
Keck I                                  LONEOS Schmidt
Uppsala Schmidt                         Oschin Schmidt
Isaac Newton Telescope                  Hale reflector
Jacobus Kapteyn Telescope               Perkins reflector
GEODSS telescope                        Plaskett telescope
Subaru Telescope                        SoTIE reflector
SALT                                    MMT
Calar Alto reflector                    CTIO reflector
WIYN reflector                          Gemini North
Gemini South                            VLT UT1
VLT UT2                                 Lowell Observatory Discovery Channel telescope
Discovery Channel Telescope             Magellan-Baade telescope
Magellan-Clay telescope
```

A number of common abbreviations of the above-listed named telescopes are
also allowed. These are expanded to the full name by the processing code:

```
UoH  -> University of Hawaii
CFHT -> Canada-France-Hawaii Telescope
NTT  -> New Technology Telescope
NOT  -> Nordic Optical Telescope
INT  -> Isaac Newton Telescope
```

Requests to allow further named professional instruments will be entertained.


## 7: Defined Extras

The list of extras is as follows:

```
prime-focus corrector    90prime camera           EMMI-RILD system
WFI system               MegaCam
```

Requests to allow further extras will be entertained.
