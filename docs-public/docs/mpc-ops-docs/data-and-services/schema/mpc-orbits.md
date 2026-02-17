# Schema: mpc_orbits

The MPC orbits table contains orbits and orbital related information of minor planets, comets and natural satellites. The table is continuously updated.

## Known issues

!!! warning
    This table should be considered a work in progress.

- Comet and natural satellite orbits are not saved (for now).
- Fields are not fully populated.
- May contain orbits with secondary designations or old orbits that have not been updated.

## Useful information

- Both packed and unpacked forms are included for primary provisional designations.
- Only unpacked numbered (no parentheses) included for primary permanent designations.
- Can be linked to the current identification table using primary provisional designation fields.

| Column | Data type | Description |
|--------|-----------|-------------|
| a1 | double precision | A1 non-gravitational acceleration for comets [10^(-10) au/d^2] |
| a2 | double precision | A2 non-gravitational acceleration for comets [10^(-10) au/d^2] |
| yarkovsky | double precision | A2 Yarkovsky acceleration [10^(-10) au/d^2] |
| a3 | double precision | A3 non-gravitational acceleration for comets [10^(-10) au/d^2] |
| h | double precision | Absolute magnitude (OrbFit) |
| arc_length_total | double precision | Arc length of all observations |
| arc_length_sel | double precision | Arc length of selected observations |
| argperi | double precision | Argument of pericenter [degrees] |
| created_at | timestamp(6) without time zone | Date and time of initial row insert |
| updated_at | timestamp(6) without time zone | Date and time of latest row update |
| fitting_datetime | timestamp(6) without time zone | Date and time when orbital fit was performed |
| dt | double precision | DeltaT non-gravitational acceleration [days] |
| e | double precision | Eccentricity |
| i | double precision | Inclination [degrees] |
| node | double precision | Longitude of ascending node [degrees] |
| mean_anomaly | double precision | Mean anomaly [degrees] |
| earth_moid | double precision | MOID with Earth [au] |
| nopp | integer | Number of oppositions |
| u_param | integer | U parameter |
| mpc_orb_jsonb | jsonb | MPC JSON orbit format |
| normalized_rms | double precision | Normalized post-fit RMS |
| not_normalized_rms | double precision | Not normalized post-fit RMS [arcseconds] |
| mean_motion | double precision | Orbital mean motion [degrees/day] |
| period | double precision | Orbital period [days] |
| orbit_type_int | integer | Orbit classification |
| epoch_mjd | double precision | Orbit epoch [TT, MJD] |
| packed_primary_provisional_designation | text | Packed primary provisional designation |
| q | double precision | Perihelion distance [au] |
| a1_unc | double precision | 1-sigma uncertainty in A1 |
| a2_unc | double precision | 1-sigma uncertainty in A2 |
| yarkovsky_unc | double precision | 1-sigma uncertainty in Yarkovsky |
| a3_unc | double precision | 1-sigma uncertainty in A3 |
| argperi_unc | double precision | 1-sigma uncertainty in argument of pericenter |
| dt_unc | double precision | 1-sigma uncertainty in DeltaT |
| e_unc | double precision | 1-sigma uncertainty in eccentricity |
| i_unc | double precision | 1-sigma uncertainty in inclination |
| node_unc | double precision | 1-sigma uncertainty in longitude of ascending node |
| mean_anomaly_unc | double precision | 1-sigma uncertainty in mean anomaly |
| mean_motion_unc | double precision | 1-sigma uncertainty in mean motion |
| period_unc | double precision | 1-sigma uncertainty in period |
| q_unc | double precision | 1-sigma uncertainty in perihelion distance |
| a_unc | double precision | 1-sigma uncertainty in semi-major axis |
| srp_unc | double precision | 1-sigma uncertainty in solar radiation pressure |
| peri_time_unc | double precision | 1-sigma uncertainty in pericenter passage time |
| id | integer | PostgreSQL automatically generated identifier |
| a | double precision | Semi-major axis [au] |
| g | double precision | Slope parameter |
| srp | double precision | Solar radiation pressure [m^2/ton] |
| peri_time | double precision | Time of pericenter passage [days] |
| nobs_total | integer | Total number of observations |
| nobs_total_sel | integer | Total number of observations used by fit |
| unpacked_primary_provisional_designation | text | Unpacked primary provisional designation |

[Back to schema overview](../replicated-tables-schema.md)
