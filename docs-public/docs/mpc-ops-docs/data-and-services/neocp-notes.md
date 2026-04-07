# Notes on the NEO Confirmation Page

The [NEO Confirmation Page (NEOCP)](https://minorplanetcenter.net/iau/NEO/toconfirm_tabular.html) provides ephemerides for newly-discovered fast-moving or other unusual objects in need of confirmation. Most objects on the NEOCP do not yet have official provisional designations and are identified only by temporary observer-assigned identifiers.

!!! warning
    Temporary designations and ephemerides from the NEOCP must not be promulgated.


## Comets on the NEOCP

Due to increased comet discoveries initially appearing on the NEO Confirmation Page, the system now supports obtaining ephemerides for newly-discovered comets that do not yet have published orbits. This ensures accurate astrometry can be obtained in the period between the announcement of a comet and the publication of its first orbit.


## Observation Guidelines

- Observations should span several hours across at least one night when possible.
- Azimuths are measured westward from the south meridian.
- All ephemerides use Universal Time (UT).
- Ephemerides can be generated for the geocenter, a specific observatory code, or a user-specified location on the Earth's surface.
- Single-night observations can generate uncertainty maps and offset tables.


## Uncertainty Map Color System

Objects on the NEOCP are color-coded by their estimated distance from Earth:

| Color | Distance | Flag | Notes |
|---|---|---|---|
| Green | > 0.05 AU | | Dark blue for main-belt objects; magenta for Jupiter Trojans |
| Orange | 0.01 -- 0.05 AU | `!` | |
| Red | < 0.01 AU | `!!` | |
| Black | Approaching within ~1 lunar distance in 100 hours | `***` | |


## Object Removal Criteria

Objects are removed from the NEOCP when one or more of the following conditions are met:

1. Sufficient astrometry has been obtained to determine a well-constrained orbit, and a new designation is assigned.
2. The object is identified with a previously known object.
3. The object is classified as an artificial satellite.
4. The observations are submitted in error or retracted by the observer.
5. The object is linked to another object already on the NEOCP.
6. The object cannot be confirmed due to insufficient follow-up astrometry (see [automatic removal conditions](#automatic-removal-conditions) below).


## Automated Designation Requirements

An automated script assigns provisional designations to NEOCP objects only when **all** of the following conditions are met:

1. The observation arc spans at least one day, with 10 or more observations.
2. Variant orbits are consistently classified (all NEO or all non-NEO).
3. The perihelion distance is less than 5.6 AU.
4. Astrometry has been received from at least 2 observatory codes across at least 3 separate submissions.
5. The object is not flagged as an artificial satellite.
6. The object is not flagged as a comet.
7. At least 3 photometric measurements are available.
8. No near-duplicate observations exist in the database.
9. The orbit fit is well-constrained and non-degenerate.
10. An associated H-magnitude is included in the orbit fit.
11. More than 85% of observations are used in the fit.
12. Residuals are clean, without suspicious patterns.
13. There are no virtual impactors or concerning close approaches.
14. The Earth MOID is greater than 2 Earth radii, with no close approaches within 5 Earth radii during the 21st century.
15. The designation does not exceed [packed designation](../designations/packed-designations.md) limits.
16. All fail-safe checks pass.


## Automatic Removal Conditions

Unconfirmed objects are automatically removed from the NEOCP if:

- The object has been listed for 5 or more days and the observation arc is less than 0.833 day.
- No positive cometary activity has been reported.
- **And** one of the following applies:
    - The median V-magnitude is fainter than 24.5.
    - The solar elongation is less than 30 degrees.
    - The object has been on the NEOCP for 20 or more days.
    - The positional uncertainty exceeds magnitude-dependent thresholds:
        - 30 degrees at V < 18
        - 10 degrees at V < 20
        - Declining thresholds at fainter magnitudes

Objects with longer arcs but unconstrained orbits may remain on the NEOCP beyond 20 days, subject to manual removal.
