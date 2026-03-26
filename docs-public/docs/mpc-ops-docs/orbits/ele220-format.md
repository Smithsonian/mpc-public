# ele220 Format

The ele220 format is an old 220-character string that was created for internal use at the MPC for storing minor planet orbital computation data.

!!! warning "Deprecation Notice"
    The MPC will deprecate the ele220 format in favor of a new orbit format. This page is provided for reference only.

**Limitations:**

- Only applies to asteroids; comets and natural satellites are excluded
- Cannot represent parabolic or hyperbolic orbits
- Orbital elements appear twice with differing precision levels


## Field Specifications

| Character Range | Field Description |
|---|---|
| 0-7 | Packed designation |
| 7-12 | Slope parameter G |
| 12-24 | Packed time of pericenter passage |
| 24-34 | Argument of perihelion, J2000.0 (degrees) |
| 34-44 | Longitude of ascending node, J2000.0 (degrees) |
| 44-54 | Inclination to ecliptic, J2000.0 (degrees) |
| 54-64 | Perihelion distance (AU) |
| 64-74 | Eccentricity |
| 75-80 | Epoch (packed form, TT) |
| 80-90 | Designation (unpacked) |
| 91-96 | Absolute magnitude H |
| 97-102 | Epoch (packed form, TT) |
| 103-108 | Mean anomaly at epoch (degrees) |
| 109-114 | Argument of pericenter, J2000.0 (degrees) |
| 115-120 | Longitude of ascending node, J2000.0 (degrees) |
| 121-126 | Inclination to ecliptic, J2000.0 (degrees) |
| 127-132 | Eccentricity |
| 133-140 | Semi-major axis (AU) |
| 141-144 | Number of oppositions |
| 144-150 | Arc length or observation year range |
| 150-156 | Number of observations |
| 157 | MPC U parameter |
| 159-168 | Computer name |
| 169-178 | Publication reference |
| 179-184 | Time of first observation (packed form) |
| 185-190 | Time of last observation (packed form) |
| 190-196 | Post-fit RMS |
| 197 | Perturber scheme |
| 199-202 | Coarse perturber indicator |
| 203-207 | Precise perturber indicator |
| 208-210 | Propagator step-size (internal use only) |
| 212-214 | Packed 'numberability' score |
| 214 | Current opposition score |
| 215-222 | RUNOFF score |


## Related

- [Indication of perturbing bodies](perturbers.md)
- [Export orbit formats (overview)](orbit-format-overview.md)
- [MPC_ORB JSON format](mpc-orb-json.md)
