# Indication of Perturbing Bodies

The Minor Planet Center maintains files of perturbed orbital elements that specifically identify the source of planetary ephemerides and additional perturbing bodies beyond Mercury through Neptune.


## One-Line Format Changes

Changes affect the one-line format for orbit submissions to the Minor Planet Center. Columns 1-201 and 210-220 remain unaffected. The "Extended Computer Service" includes this information, though printed MPCs omit it for simplicity.


## Column 202: Planetary Ephemerides Descriptor

This column identifies the system used for perturbing planets:

| Code | Ephemeris |
|------|-----------|
| (space) | Undefined/unknown; assumes JPL DE200 positions + masses |
| d | JPL DE200 positions + masses |
| f | JPL DE245 positions + masses |
| h | JPL DE403 positions + masses |
| j | JPL DE405 positions + masses |
| k | JPL DE431 positions + masses |
| l | JPL DE441 positions + masses |

New codes are assigned only under exceptional circumstances, as consistency in perturbation schemes takes priority over frequent updates.


## Columns 204-206: Coarse Perturbing Bodies Indicator

Minor planets now use lowercase letters, distinguishing between M-P (includes Pluto) and M-p (includes Pallas and likely Ceres).


## Columns 208-209: Precise Perturbers (Hexadecimal)

A two-digit hexadecimal number indicates specific perturbers:

**Low digit:**

| Perturber | Bit | Value |
|-----------|-----|-------|
| Hygiea | 0 | 1 |
| Earth | 1 | 2 |
| Moon | 2 | 4 |
| Ceres | 3 | 8 |

**High digit:**

| Perturber | Bit | Value |
|-----------|-----|-------|
| Pallas | 0 | 1 |
| Vesta | 1 | 2 |
| Eunomia | 2 | 4 |

Note: Low-digit bits 1 and 2 must both be set or both be unset (Earth and Moon constraint).


## Examples

| Coarse | Precise | Perturbers |
|--------|---------|------------|
| M-c | 08 | Ceres, EM barycenter |
| M-c | 0E | Ceres, Earth, Moon |
| M-p | 16 | Pallas, Earth, Moon (NOT RECOMMENDED) |
| M-p | 18 | Ceres, Pallas, EM barycenter |
| M-p | 1E | Ceres, Pallas, Earth, Moon |
| M-v | 38 | Ceres, Pallas, Vesta, EM barycenter |
| M-v | 3E | Ceres, Pallas, Vesta, Earth, Moon |
| M-e | 78 | Ceres, Pallas, Vesta, Eunomia, EM barycenter |
| M-e | 7E | Ceres, Pallas, Vesta, Eunomia, Earth, Moon |
| M-h | 39 | Ceres, Pallas, Vesta, Hygiea, EM barycenter |


## Default Settings

The default for Minor Planet Center orbits is k (DE431), M-v (coarse) and 38 or 3E (precise, depending on whether the object is an Earth-approacher or not). Additional perturbers are incorporated as needed.
