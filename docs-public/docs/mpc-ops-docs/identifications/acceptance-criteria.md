# Criteria for Accepting or Rejecting Identifications


## Submissions Rejected Without Orbit Fitting

### ITF-to-ITF submissions

!!! note
    The criteria below do not apply to NEOCP objects.

The MPC will reject ITF-to-ITF identifications without performing any orbit fitting if
any of the following is true:

- The submission format is incorrect. See the
  [submission format description](../apis/identifications.md).
- The submitted tracklets cover less than 3 distinct nights.
- The arc length covered by the tracklets is less than 3 days.
- The number of nights is 3 and the arc length is larger than 15 days.
- You are trying to submit a two apparition linkage when the second apparition is
  represented only by a single tracklet regardless of the number of tracklets in the
  first apparition.
- The arc starts and ends with a single detection tracklet.


### ITF-to-DES submissions

The MPC will reject ITF-to-DES identifications without performing any orbit fitting if
any of the following is true:

- The submission format is incorrect. See the
  [submission format description](../apis/identifications.md).
- You are trying to extend the orbit of a one-apparition non-NEO to a two-apparitions
  non-NEO using only one single tracklet over one night (arc length < 0.75 days). Please
  note that this criteria does not apply to NEOs. See the
  [Recovery Page](https://minorplanetcenter.net/iau/recovery/recovery.html) for further
  explanation.


### DES-to-DES submissions

The MPC will reject DES-to-DES identifications without performing any orbit fitting if
any of the following is true:

- The submission format is incorrect. See the
  [submission format description](../apis/identifications.md).
- You are attempting to link together two only one-opposition distant objects (q>5.5).


---

## Submissions Rejected With Orbit Fitting

### ITF-to-ITF submissions

!!! note
    The criteria below do not apply to NEOCP objects.

The MPC will reject certain identifications after performing an orbit fit if any of the
following is true:

- If the tracklets cover exactly 3 nights, have an arc length < 15 days and RMS > 0.25"
  and orbit quality is not sufficient (defined below).
- If the tracklets cover more than 3 nights, have an arc length < 10 days and RMS >
  0.25" and orbit quality is not sufficient (defined below).
- The orbit fit did not converge.

**Minimum orbit quality definition for 3-nighters:** Covariance requirements on the
converged orbit: The 1-sigma range for the orbital elements must satisfy the following:
semimajor-axis < 0.05 AU, perihelion distance < 0.05 AU, inclination < 0.5 deg,
eccentricity < 0.05; and the eccentricity of the orbit must be < 0.5.

MPC accepts multi-opposition ITF-to-ITF submissions when:

- for 2-opposition orbits, one apparition must have at least 3 nights, the other
  apparition at least two nights; or
- for 3-opposition and 4-opposition orbits, at least one apparition must have at least
  3 nights;
- for 5 or more oppositions, at least one apparition must have at least 3 nights, or at
  least two apparitions must have two nights each.

New apparitions are counted by gaps between subsequent nights being longer than 237 days.


### ITF-to-DES submissions

The MPC will reject certain identifications after performing an orbit fit if any of the
following is true:

- The orbit fit did not converge.


### DES-to-DES submissions

The MPC will reject certain identifications after performing an orbit fit if any of the
following is true:

- The orbit fit did not converge.
