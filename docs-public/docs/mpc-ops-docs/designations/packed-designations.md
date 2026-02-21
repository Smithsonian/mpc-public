# Packed Provisional and Permanent Designations

This document describes the packed forms for provisional and permanent designations used
in MPC data files.

See also the [Provisional Designations](provisional-designations.md) page for a
description of the unpacked provisional designation formats and the
[Extended Packed Provisional Designation Scheme](provisional-designations.md#extended-packed-provisional-designation-scheme)
for the new base-62 scheme designed for the LSST era.

---

## Provisional Designations

The provisional designation stored in the orbit and observations uses a
7-character packed format that saves space.

### Minor Planets

A fulsome description of the packed format for the provisional designations of minor planets is provided on 
the [provisional-designations](../provisional-designations/#packed-provisional-designations)
page. 


### Comets

Columns 1-4 are as detailed above for minor planets. Columns 5-6 contain the order
within the half-month period. Column 7 will normally be '0', except for split comets,
when the fragment designation is stored there as a lower-case letter.

```
   Examples:
   1995 A1    = J95A010
   1994 P1-B  = J94P01b   refers to fragment B of 1994 P1
   1994 P1    = J94P010   refers to the whole comet 1994 P1
   2048 X13   = K48X130
   2033 L89-C = K33L89c
   2088 A103  = K88AA30   A3 = 103
```

Comet designations may also be given in a 12-character form, where columns 6-12 are as
described above. Column 5 will contain a 'C', 'P', 'D' or 'X' (depending on the status
and orbit type of the comet). For a numbered periodic comet, columns 1-4 contain the
periodic-comet number, left-padded with zeroes. For other comets columns 1-4 contain
blanks.

### Natural Satellites

The packed provisional format for satellite designations is identical to the packed
format for comet designations, with the restriction that the last column (either column
7 or 12, depending on the form) always contains "0".

---

## Permanent Designations

The permanent designation stored on the orbit and observations is stored in a
5-character packed format that saves space and makes sorting easier.

### Minor Planets

If the minor-planet number is less than 100000, then the number is stored as a
zero-padded right-justified string. E.g., (3202) is stored as `03202`, (50000) as
`50000`.

When the number is above 99999, the number MOD 10000 is stored in columns 2-5 of the
string and the number DIV 10000 is represented by the letters A-Z (if between 10 and 35,
inclusive) or a-z (if between 36 and 61, inclusive). E.g., (100345) is represented as
`A0345`, (360017) as `a0017`, and (203289) as `K3289`.

Numbers above 619999 will be indicated using a tilde, `~`, as the first character. The
subsequent 4 characters will all be base-62 (0-9, then A-Z if between 10 and 35
inclusive, then a-z if between 36 and 61 inclusive) and used to store the target number
MINUS 620,000.

E.g.

- (620000) is represented as `~0000`
  (i.e. 620,000 - 620,000 = 0 = 0\*62^3 + 0\*62^2 + 0\*62^1 + 0\*62^0).
- (620061) is represented as `~000z`
  (i.e. 620,061 - 620,000 = 61 = 0\*62^3 + 0\*62^2 + 0\*62^1 + 61\*62^0).
- (3140113) is represented as `~AZaz`
  (i.e. 3,140,113 - 620,000 = 2,520,113 = 10\*62^3 + 35\*62^2 + 36\*62^1 + 61\*62^0).
- (15396335) is represented as `~zzzz`
  (i.e. 15,396,335 - 620,000 = 14,776,335 = 61\*62^3 + 61\*62^2 + 61\*62^1 + 61\*62^0).

### Comets

Permanent designations for comets are only given to periodic comets seen to return (or
for Centaur comets, seen at multiple apparitions). The comet number is stored zero-padded
right-justified in columns 1-4. Column 5 usually contains "P", except for lost or
defunct periodic comets when it contains "D".

### Natural Satellites

Permanent designations for natural satellites are the Roman numerals. A permanent
natural-satellite packed designation starts with a letter indicating to which planet the
satellite belongs ("J" = Jupiter, "S" = Saturn, "U" = Uranus, "N" = Neptune), followed
by a three-character zero-padded right-justified string containing the numerical
representation of the Roman numeral, followed by "S". E.g., Jupiter XIII is represented
as `J013S`, Saturn X as `S010S` and Neptune II as `N002S`.
