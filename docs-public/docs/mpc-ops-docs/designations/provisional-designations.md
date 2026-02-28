# Provisional Designations for Minor Planets

This page describes the formats for provisional designations of minor planets, including
current (post-1925) and old-style (pre-1925) unpacked designations, as well as the
packed provisional designation schemes used in MPC data files.

---

## Unpacked Provisional Designations

### Current Provisional Designations (Post-1925)

The Minor Planet Center assigns new provisional designations when an object cannot be
identified immediately with some already designated object and the orbit of the object
is good enough to not require immediate additional follow-up.

The standard designation consists of the following parts, all of which are related to
the date of discovery of the object: a 4-digit number indicating the year; a space; a
letter to show the half-month; another letter to show the order within the half-month;
and an optional number to indicate the number of times the second letter has been
repeated in that half-month period.

The half-month of discovery is indicated using the following scheme:

```
  Letter     Dates             Letter      Dates
    A      Jan. 1-15             B       Jan. 16-31
    C      Feb. 1-15             D       Feb. 16-29
    E      Mar. 1-15             F       Mar. 16-31
    G      Apr. 1-15             H       Apr. 16-30
    J      May  1-15             K       May  16-31
    L      June 1-15             M       June 16-30
    N      July 1-15             O       July 16-31
    P      Aug. 1-15             Q       Aug. 16-31
    R      Sept.1-15             S       Sept.16-30
    T      Oct. 1-15             U       Oct. 16-31
    V      Nov. 1-15             W       Nov. 16-30
    X      Dec. 1-15             Y       Dec. 16-31

             I is omitted and Z is unused
```

The order within the month is indicated using letters as follows:

```
    A = 1st     B = 2nd     C = 3rd     D = 4th     E = 5th
    F = 6th     G = 7th     H = 8th     J = 9th     K = 10th
    L = 11th    M = 12th    N = 13th    O = 14th    P = 15th
    Q = 16th    R = 17th    S = 18th    T = 19th    U = 20th
    V = 21st    W = 22nd    X = 23rd    Y = 24th    Z = 25th

                        I is omitted
```

If there are more than 25 discoveries in any one half-month period, the second letter
is recycled and a numeral '1' is added to the end of the designation. If there are more
than 50 discoveries, the second-letter is again recycled, with a numeral '2' appended
after the second letter. Discoveries 76-100 have numeral '3' added, numbers 101-125
numeral '4', etc. When possible, these additional numbers should be indicated using
subscript characters.

Thus the order of assignment of designations in a particular half-month period is as
follows: `1995 SA, 1995 SB, ..., 1995 SY, 1995 SZ, 1995 SA1, ..., 1995 SZ1, 1995 SA2, ..., 1995 SZ2, ..., 1995 SA10, ..., 1995 SZ10,` etc.

This scheme has been extended to pre-1925 discoveries -- such designations are indicated
by the replacement of the initial digit of the year by the letter 'A'. Thus, `A904 OA`
is the first object designated that was discovered in the second half of July 1904.


### Survey Designations

Four special surveys, undertaken between 1960 and 1977, have designations that consist
of a number (identifying the order within that survey), a space and a survey identifier.
The survey identifiers are as follows:

```
   Survey                         Identifier
   Palomar-Leiden (1960)             P-L
   First Trojan Survey (1971)        T-1
   Second Trojan Survey (1973)       T-2
   Third Trojan Survey (1977)        T-3
```

Example designations are `2040 P-L, 3138 T-1, 1010 T-2 and 4101 T-3`.


### Old-Style Provisional Designations (Pre-1925)

In the first half of the 19th century, minor planets were referred to simply by name.
The assignment of ordinal numbers, ostensibly in order of discovery, was introduced in
the early 1850s. Initially, new numbers were assigned by the editors of the
*Astronomisches Nachrichten (AN)* immediately upon receipt of the announcement of a new
discovery from an observer.

In 1892 a system of provisional designations was introduced by the *AN*. A definitive
number was subsequently given by the editors of the *Berliner Astronomisches Jahrbuch*
to those objects for which reasonable orbital elements had been computed. The provisional
designation scheme consisted initially of a year and a single letter: e.g., 1892 A,
1892 B, etc., omitting the letter 'I'.

In 1893, the 25 available letters proved to be insufficient and a series of double
letter designations was introduced: e.g. 1893 AA, 1893 AB, etc., omitting the letter
'I'. The sequence of double letters was not restarted anew each year, so 1894 AQ
followed 1893 AP (for example). In 1916, the letters reached ZZ and, rather than
starting a series of triple-letter designations, the double-letter series was restarted
with 1916 AA.

!!! note
    In old publications, it is common to see 'J' as the omitted letter instead of
    'I' -- the sequence going 1892 H, 1892 I, 1892 K, etc. Modern usage would consider
    1892 I to be the same as 1892 J and it is this latter designation which is recorded.

In the double-letter scheme it was not generally possible to insert new discoveries into
the sequence once designations had been assigned in a subsequent year. The scheme used
to get round this problem was rather clumsy and used a designation consisting of the
year and a lower-case letter in a manner similar to the old provisional-designation
scheme for comets. For example, 1915 a (note that there is a space between the year and
the letter in order to distinguish this designation from the old-style comet designation
1915a), 1917 b. In 1914 designations of the form year plus Greek letter were used in
addition.

During World War I the active observers at Simeis in the Crimea, deprived of official
designations for their discoveries, assigned their own. The designations came in two
forms: year + Greek capital sigma + letter(s); Greek capital sigma + number. The Greek
capital sigma is indicated as SIGMA.

Other designation schemes used at Simeis and other observatories are listed on the
[Temporary Minor Planet Designations](temporary-designations.md) page.

---

To summarise, the following forms of old-style input are valid:

- Year + Single Letter: `1892 A`
- Year + Double Letter: `1914 VV`
- Year + letter: `1913 a`
- Year + Greek letter: `1914 gamma`
- Year + SIGMA + letter: `1915 SIGMA r, 1916 SIGMA ci`
- SIGMA + number: `SIGMA 27`

For the purposes of searching, `SIGMA` may be abbreviated to `SIG` and the year is
optional on the `year+SIGMA+letter` designations (i.e., `SIGMA ci` is a shorthand form
for `1916 SIGMA ci`).

---

## Packed Provisional Designations

The Minor Planet Center (MPC) uses *packed provisional designations* to communicate
designation information within the orbit and observations (MPC1992 80-character) format.

See also the [Packed Provisional and Permanent Designations](packed-designations.md)
page for the complete specification of packed formats including permanent designations
for minor planets, comets, and natural satellites.


### Original Packed Provisional Designation Scheme

The first two digits of the year are packed into a single character in column 1
(I = 18, J = 19, K = 20). Columns 2-3 contain the last two digits of the year.
Column 4 contains the half-month letter and column 7 contains the second letter. The
cycle count (the number of times that the second letter has cycled through the alphabet)
is coded in columns 5-6, using a letter in column 5 when the cycle count is larger than
99. The uppercase letters are used, followed by the lowercase letters.

Where possible, the cycle count should be displayed as a subscript when the designation
is written out in unpacked format.

```
   Examples:
   J95X00A = 1995 XA
   J95X01L = 1995 XL1
   J95F13B = 1995 FB13
   J98SA8Q = 1998 SQ108
   J98SC7V = 1998 SV127
   J98SG2S = 1998 SS162
   K99AJ3Z = 2099 AZ193
   K08Aa0A = 2008 AA360
   K07Tf8A = 2007 TA418
```

Survey designations of the form 2040 P-L, 3138 T-1, 1010 T-2 and 4101 T-3 are packed
differently. Columns 1-3 contain the code indicating the survey and columns 4-7 contain
the number within the survey.

```
   Examples:
   2040 P-L  = PLS2040
   3138 T-1  = T1S3138
   1010 T-2  = T2S1010
   4101 T-3  = T3S4101
```


### Extended Packed Provisional Designation Scheme

As described in the [October 2023 Newsletter](https://minorplanetcenter.net/media/newsletters/MPC_Newsletter_Oct2023.pdf),
the original packed provisional designation scheme has hitherto been limited to
supporting only 15,500 new designations per half month (the standard unpacked
designations described above have no such restrictions). When the Vera Rubin LSST
commences operations, it is estimated that during its most productive months,
approximately 250,000 objects will be discovered. To allow the community to continue
using the orbit and observations files containing the packed provisional designation
format while accommodating the predicted volume of LSST discoveries, the MPC is
extending the packing-format as described below.

When more than 15,500 objects are designated within a half-month, designations will be
indicated as follows:

- The first character must be an underscore, simultaneously indicating (a) the use of
  the extended packed provisional format, and (b) that the first 2 digits of the year
  of discovery are 20.

    !!! note
        This implies that the extended packed provisional designation format will not be
        applied to objects discovered prior to 2010 (see next point for the encoding of
        the last two digits of the year).

- The second character must be a capital letter (indicating the last 2 digits of the
  year of discovery, where 'P' = 25, 'Q' = 26, etc).

    !!! note
        This encoding scheme is the same as that used for the first two digits of the
        year in the original packed provisional designation format. This implies that
        this extended packed provisional designation format is not expected to be employed
        beyond 2035 (as 'Z' = 35).

- The third character is the capital letter for the half month.
- Four alphanumeric characters [0-9A-Za-z] will be used as a base-62 representation of
  the order of designation after 15,500.

    !!! note
        This implies subtracting 15,501 from the sequence-number before converting to the
        base-62 representation. The base-62 representation uses the digits 0-9 to
        represent numbers from 0-9, then upper-case letters A-Z to represent numbers
        between 10 and 35 inclusive, then lower-case letters a-z to represent numbers
        between 36 and 61 inclusive.

As such:

- The *15,500th* object designated in half-month "C" of 2026 will be *2026 CZ619 == K26Cz9Z*
- The *15,501st* object designated in half-month "C" of 2026 will be *2026 CA620 == \_QC0000*
- The *154,775th* object designated in half-month "C" of 2026 will be *2026 CZ6190 == \_QC0aEM*
- The final object designated in half-month "C" of 2026 that can be accommodated in this
  extended format will be number *14,791,836*, i.e. *2026 CL591673 == \_QCzzzz*. This
  seems likely to be sufficient.

Some example designations are provided below to help elucidate the packed provisional
designation in a variety of cases.

| Year | Half Month | Order (Integer) | Order (Alpha-Numeric) | Order minus 15501 (Integer) | Unpacked | Packed |
|------|------------|-----------------|----------------------|----------------------------|----------|--------|
| 2023 | B | 1 | A | - | 2023 BA | K23B00A |
| 2024 | C | 100 | Z3 | - | 2024 CZ3 | K24C03Z |
| 2025 | D | 15500 | Z619 | - | 2025 DZ619 | K25Dz9Z |
| 2025 | D | 15501 | A620 | 0 | 2025 DA620 | \_PD0000 |
| 2026 | D | 15524 | Y620 | 23 | 2026 DY620 | \_QD000N |
| 2027 | E | 154775 | Z6190 | 139274 | 2027 DZ6190 | \_RD0aEM |
| 2028 | E | 8493726 | A339749 | 8478225 | 2028 EA339749 | \_SEZZZZ |
| 2029 | F | 14791836 | L591673 | 14776335 | 2029 FL591673 | \_TFzzzz |


#### Extended Packed Provisional Designations for Asteroids Redesignated as Comets

Objects that were originally designated as minor planets but subsequently exhibit
cometary activity may be redesignated as comets. When this happens, the redesignated
object retains the original asteroid designation with the addition of a prefix that is
either P/ (periodic), C/ (non-periodic, long periodic), X/ (no reliable orbit could be
calculated, historical), D/ (comet that has disappeared, broken or lost), A/ (object on
near-parabolic and likely cometary orbit without any activity) or I (interstellar). The
final designation will thus follow the extended packed format described above. Explicit
examples are provided in the table below.

| Year | Half Month | Order (Integer) | Order (Alpha-Numeric) | Order minus 15501 (Integer) | Unpacked | Packed |
|------|------------|-----------------|----------------------|----------------------------|----------|--------|
| 2023 | B | 1 | A | - | P/2023 BA | PK23B00A |
| 2024 | C | 100 | Z3 | - | C/2024 CZ3 | CK24C03Z |
| 2025 | D | 15500 | Z619 | - | A/2025 DZ619 | AK25Dz9Z |
| 2025 | D | 15501 | A620 | 0 | P/2025 DA620 | P\_PD0000 |
| 2026 | D | 15524 | Y620 | 23 | C/2026 DY620 | C\_QD000N |
| 2027 | E | 154775 | Z6190 | 139274 | A/2027 DZ6190 | A\_RD0aEM |
| 2028 | E | 8493726 | A339749 | 8478225 | C/2028 EA339749 | C\_SEZZZZ |
| 2029 | F | 14791836 | L591673 | 14776335 | P/2029 FL591673 | P\_TFzzzz |

The MPC will not publish any designations using this extended packed provisional
designation format before June 2024. After that date the MPC will begin publishing
designations in the extended format as necessary in any publications.


