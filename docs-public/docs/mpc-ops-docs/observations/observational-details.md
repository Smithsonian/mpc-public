# Specifying Observational Details

Observers submitting observations by electronic means (generally e-mail) are required to
include observer, measurer and telescope details in every submission.

!!! note
    Observation batches that do not include an observational header will not
    be recognized as containing observations by the automated processes and
    will be ignored.

The observational details are to be contained in a series of header lines,
beginning with certain keywords specified below and placed before any
observations.

---

## Header Keywords

- The first line must begin `COD` and be followed by a three-character
  observatory code. If you are reporting observations from a new
  site, you must specify `XXX` as the observatory code.
- The `CON` keyword is optional for most observers, but must be given for
  observations made at sites which use program codes. The `CON` line must
  be the second line in the header and must contain as its first element the
  contact name. Additional contact details may then follow.
- Other lines, which may follow in any order, begin:
    - `OBS` (followed by the list of observers, no programs)
    - `MEA` (followed by the list of measurers, no programs)
    - `TEL` (followed by [details of the telescope](telescope-details.md))
    - `NET` (followed by the abbreviated name(s) of the catalogue(s) used for the reductions)
    - `BND` (followed by single character representing the mag band used for magnitude estimates)
    - `COM` (followed by a textual comment)
    - `NUM` (followed by a count of the observations in this batch)
- An additional keyword, `ACK`, enables the [Minor Planet Center](https://minorplanetcenter.net/iau/mpc.html)
  to automatically acknowledge receipt of your observations.
  The text on the `ACK` line will be e-mailed back to you to let you know that your e-mail arrived.
  If it is necessary to communicate designations to you, these will be sent after the batch is processed.
  Some types of objects require special handling; for these, particular words/phrases must be included in the `ACK` line.
  See [MPEC 2018-W60](https://www.minorplanetcenter.net/mpec/K18/K18W60.html) and the list towards the bottom of this page for information on what should be included in the `ACK` line.
- `AC2` (followed by list of e-mails) must be supplied for cURL submissions, optional for e-mail submissions.
  By default, the acknowledgement is sent to the e-mail address from which
  the original message was sent. You can override this default
  behavior by specifying the `AC2` keyword, following it by one or more
  Internet-style e-mail address, e.g.:

    ```
    AC2 scully@fbi.gov,mulder@fbi.gov
    ```

    The only restriction of the number of e-mail addresses is that the total
    length of the line (including the four characters `AC2 `) must be less than
    or equal to 80 characters. Note that any e-mail address specified with the
    `AC2` keyword is NOT enclosed within square brackets. Any of the e-mail
    addresses specified can be forwarding addresses at your local site.


## Formatting Requirements

- All lines must be 80 columns or less in width.
- The keywords must be in capitals and begin in column 1.
- The keyword must be followed by a space (ASCII 32).
- The `CON`, `OBS` and `MEA` lines may extend onto a second or subsequent line,
  repeating the keyword as necessary.
- Names of individuals must be specified as initials + surname with
  spaces separating each part of the name.
- Multiple names on the same line are separated by ", ".
- Initials given must be as given on official documents (e.g., passports,
  driving licenses, etc.). If your name is 'Robert', but you use 'Bob'
  in day-to-day usage, you must still specify your initial as 'R.' not 'B.'.
- Names must be specified as mixture of capital and lower-case letters,
  they must be separated from any following name(s) by a comma and they
  must not be broken across lines.
- If more than one initial is given, there must be a space between each of
  the initials: e.g., 'J. R. R. Tolkien'.
- Hyphenated first names should be abbreviated with the hyphen: e.g.,
  'Jean-Francois Hulot' would be 'J.-F. Hulot'.
- Names that contain characters with diacritical marks (e.g., accents or cedillas such as `à`, `ç`, or `ü`)
  may be specified using [standard TeX notation](../data-and-services/non-english-characters.md) -- alternatively, an
  explanation of any special characters required must be included above
  the header.
- When there are multiple versions of the `NET` catalogue, be sure to include
  the version identifier. Don't simply specify "USNO" or "GSC": write them
  as, for example, "USNO-B1.0" or "GSC-2.2".
- Specification of telescopes must follow the following format: aperture,
  focal ratio (optional), type of instrument and CCD specifier. Do not
  specify specific brands of CCD. Do not split telescope details across
  different `TEL` lines. Valid examples are `1.0-m f/4.3 reflector + CCD` or `0.28-m f/6 Schmidt-Cassegrain + CCD`. Further information on
  [telescope details is available](telescope-details.md).
- All keywords may be repeated within the body of observations
  as required. The values associated with repeated keywords apply from the
  time they are first defined to the time that they are redefined.
- The contact's e-mail address must be specified within square brackets in
  the Internet style. Please note that e-mail addresses are given ONLY
  for the contact person.
- Only one contact name and address may be given.
- Some types of objects need special handling; submissions containing such objects must include certain words/phrases in order to insure that they are processed correctly. These words/phrases must either be included in the `ACK` header line (preferred) or in the e-mail subject line (only for e-mail submissions in the 80-character format), and are not case sensitive:
    - "NEOCP" (Submissions containing observations currently on the NEOCP)
    - "PCCP" (Submissions containing observations currently on the PCCP)
    - "NEW NEO" or "NEO CANDIDATE" (Submissions containing observations of New NEO Candidates)
    - "NEW NATURAL SATELLITE" or "NEW SATELLITE" (Submissions containing observations of New Natural Satellite Candidates)
    - "NEW TNO" or "NEW KBO" or "NEW DISTANT" or "NEW CENTAUR" (Submissions containing observations of new TNO/Centaur Candidates)
    - "NEW COMET" (Submissions containing observations of New Comet Candidates)


## Examples

Examples of valid headers are as follows:

```
COD 500
CON S. Holmes, 221B Baker Street, London NW1 4JW, England
CON [sholmes@mycroft.holmes.gov.uk]
OBS H. Poirot, P. Mason, L. Columbo, C. Chan
MEA J. Watson
TEL 0.50-m f/3.0 reflector + CCD
NET GSC-1.0
ACK Batch 001: five new tnos
AC2 dwatson@mycroft.holmes.gov.uk
```

```
COD 500
OBS D. K. Scully, F. W. Mulder, W. Skinner
ACK Batch 042: The truth is in here
```

The second example shows the minimal header that should be supplied:
the contact address, telescope and catalogue details will be taken from a
default file, and the list of measurers will be assumed to be the same as
the list of observers. You should only use the minimal header form
if you are the only observer at that code: don't use the form for sites
with multiple programs.

The format of the `TEL` and `NET` lines must be
as illustrated in recent [*MPCs*](https://minorplanetcenter.net/iau/services/MPCServices.html) (note that
specific makes of CCD are not mentioned).


## New Observatory Codes

If this is your first submission and your observing site does not yet have
an observatory code, this must be specified as:

```
COD XXX
```

An observatory code will be supplied upon acceptance of the observations
for publication.


## Program Codes

If your observatory code distinguishes between different programs you
may specify the program code after the observatory code, as in the following example:

```
COD 675 4
```

Note that program codes are assigned by the MPC, not the observer.


## Incorrect Header Examples

The following examples show **incorrect** headers (with the reason(s)
given in parentheses on the offending line(s)):

```
COD 500
OBS J.M. Jarre          (Initials in name not separated by a space)

COD 500
OBS Vangelis Papathanassiou              (First name in full, rather than initial)
MEA M. OLDFIELD                          (Name entirely in capitals)
TEL 0.50-m f/4.5 reflector + Graff1 CCD  (Make of CCD must not be mentioned)
NET Guide Star Catalogue                 (Use abbreviation GSC)

OBS J. Garcia           (No COD line)

OBS P. McCartney
COD 500                 (COD line must come first)
```
