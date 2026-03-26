# Uncertainty Parameter U and Orbit Quality Codes

## Uncertainty Parameter U

The Minor Planet Center quantifies uncertainty in perturbed orbital solutions using the
uncertainty parameter *U*, an integer in the range 0--9. A value of 0 indicates a very
small uncertainty and 9 an extremely large uncertainty. In practice, *U* is rarely
larger than 6.

### Calculation Method

The *U* value is derived from the in-orbit longitude runoff, `RUNOFF`, in seconds of arc
per decade:

```
RUNOFF = (dT * e + 10 / P * dP) * ko / P * 3600 * 3
```

where:

- **dT** = uncertainty in perihelion time (days)
- **e** = eccentricity
- **P** = orbital period (years)
- **dP** = uncertainty in orbital period (days)
- **ko** = Gaussian constant in degrees = 180 / pi * 0.01720209895
- **3600** = conversion factor to seconds of arc
- **3** = empirical factor for realistic error modeling

The conversion from RUNOFF to *U* is:

```
CONS = ln(648000) / 9           (CONS ~ 1.49)
U    = INT(ln(RUNOFF) / CONS) + 1    (0 <= U <= 9)
```

where `ln` is the natural logarithm and `INT` returns the largest integer smaller than
the argument.

### U Value Reference Table

| U | RUNOFF (arcsec/decade) | U | RUNOFF (arcsec/decade) |
|---|------------------------|---|------------------------|
| 0 | < 1.0                 | 5 | < 1692                 |
| 1 | < 4.4                 | 6 | < 7488                 |
| 2 | < 19.6                | 7 | < 33121                |
| 3 | < 86.5                | 8 | < 146502               |
| 4 | < 382                 | 9 | > 146502               |

The *U* value should not be used as a predictor for the uncertainty in the future motion
of NEAs.

---

## Orbit Quality Codes

For long-period comets, orbit quality codes replace the *U* value. These are based on
the integer orbit code *Q* from Marsden et al. (1978).

| Q        | Quality Code |
|----------|--------------|
| 9, 8     | 1A           |
| 7        | 1B           |
| 6        | 2A           |
| 5        | 2B           |
| 4        | 3A           |
| 3        | 3B           |
| 2, 1, 0  | 4            |

Codes 1A and 1B are the highest quality, used for orbits with long observed arcs and
full consideration of perturbations. The codes 3A, 3B, and 4 represent logical
extensions beyond the original scheme.
