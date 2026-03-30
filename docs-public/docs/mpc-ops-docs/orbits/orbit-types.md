# Orbit Type Definition

The Minor Planet Center classifies orbits based on osculating orbital elements. 
Objects are grouped into three main regions of the solar system.


The following parameter definitions are used in the classification criteria:
- **a** -- semimajor axis (AU)
- **q** -- perihelion distance (AU)
- **Q** -- aphelion distance (AU)
- **e** -- eccentricity
- **i** -- inclination (degrees)
- **T** -- Tisserand parameter with respect to Jupiter
- **q_Mars** = 1.405 AU (Mars perihelion distance)
- **a_Jupiter** = 5.204 AU
- **a_Neptune** = 30.178 AU


---

## Inner Solar System

Objects with orbits primarily interior to Mars' orbit.

| Type   | Code | Definition |
|--------|------|------------|
| Atira  | 0    | a < 1 and Q < 0.983 |
| Aten   | 1    | a < 1 and Q >= 0.983 |
| Apollo | 2    | a >= 1 and q < 1.017 |
| Amor   | 3    | a >= 1 and 1.017 <= q < 1.3 |
| Other  | 9    | a >= 1 and Q < q_Mars, unclassified otherwise |

---

## Middle Solar System

OObjects that occupy the orbital region of Mars-crossers up to that of the Jovian Trojans.

| Type            | Code | Definition |
|-----------------|------|------------|
| Mars Crosser    | 10   | 1 <= a < 3.2 and 1.3 < q < 1.666 |
| Main Belt       | 11   | 1 <= a < 3.27831 and i < 75 |
| Jupiter Trojan  | 12   | 4.8 < a < 5.4 and e < 0.3 |
| Other           | 19   | a < a_Jupiter, unclassified otherwise |

---

## Outer Solar System

Objects beyond Jupiter, excluding Jupiter-Coupled objects which may have smaller
semimajor axes.

| Type              | Code | Definition |
|-------------------|------|------------|
| Jupiter Coupled   | 20   | a >= 1 and 2 < T < 3 |
| Neptune Trojan    | 21   | 29.8 < a < 30.4 |
| Centaur           | 22   | a_Jupiter <= a < a_Neptune |
| TNO               | 23   | a >= a_Neptune, unclassified otherwise |

---

## Special and Unusual Orbits

| Type        | Code | Definition |
|-------------|------|------------|
| Hyperbolic  | 30   | e > 1 |
| Parabolic   | 31   | e = 1 |
| Other       | 99   | Classification failure |

---
