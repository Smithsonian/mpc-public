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

<!-- BEGIN GENERATED SCHEMA TABLE — managed by generate_public_schema_docs.py; do not edit below by hand -->

## Columns

| Column | Data type | Description |
|--------|-----------|-------------|
| `id` | integer | PostgreSQL automatically generated identifier |
| `packed_primary_provisional_designation` | text | Packed form of the primary provisional designation (e.g. K17P08M). |
| `unpacked_primary_provisional_designation` | text | Unpacked form of the primary provisional designation (e.g. 2017PM8). |
| `rwo_json` | json | This is the contents of the "rwo" file from orbfit. |
| `standard_epoch_json` | json | This is the contents of the "eq0" file from orbfit. |
| `mid_epoch_json` | json | This is the contents of the "eq1" file from orbfit. |
| `quality_json` | json | Additional quality-of-fit / results descriptors |
| `created_at` | timestamp without time zone | Date and time of initial row insert |
| `updated_at` | timestamp without time zone | Date and time of latest row update |
| `mpc_orb_jsonb` | jsonb | MPC JSON format used to describe MPC orbits. The public python package is available as part of the MPC public Gitub https://github.com/Smithsonian/mpc-public/ with additional information. |
| `moids_json` | json | Minimum orbit intersection distances (MOIDs), as JSON. |
| `stats_json` | json | Orbit-fit statistics, as JSON. |
| `ele220` | character varying(500) | Orbit encoded in the 220-character ele220 format (mutually exclusive with `ele255`). |
| `orbit_type` | integer | Integer orbit classification (see also `orbit_type_int` and the Orbit Type Definition page). |
| `is_pha` | boolean | True if the object is a Potentially Hazardous Asteroid (PHA). |
| `permid` | text | IAU permanent designation (number) for a numbered object. |
| `to_be_published` | boolean | Boolean True indicates that the orbit has been updated and requires publication |
| `publication_reference` | character varying(128) | Official reference for an orbit once published [if ""to_be_published"" is True, then ""publication_reference"" should be Null] |
| `orbit_type_int` | integer | Orbit classification based on the object orbital element. For more information please see https://minorplanetcenter.net/mpcops/documentation/orbit-types/ |
| `u_param` | integer | MPC defined U parameter. For more information please see https://www.minorplanetcenter.net/iau/info/UValue.html. |
| `nopp` | integer | MPC computed number of oppositions. |
| `arc_length_total` | double precision | Arc length of all the observations associated to the object, computed as the difference between the time of the last observations and the time of the first observation. |
| `arc_length_sel` | double precision | Arc length of all the observations selected by the fit, computed as the difference between the time of the last selected observations and the time of the first selected observation. |
| `nobs_total` | integer | Total number of observations associated to the object. |
| `nobs_total_sel` | integer | Total number of observations used by the fit. |
| `a` | double precision | Semi-major axis [au] |
| `q` | double precision | Perihelion distance [au] |
| `e` | double precision | Eccentricity |
| `i` | double precision | Inclination [degrees] |
| `node` | double precision | Longitude of the ascending node [degrees] |
| `argperi` | double precision | Argument of the pericenter [degrees] |
| `peri_time` | double precision | Time of the passage at the pericenter [days] |
| `yarkovsky` | double precision | A2 component of the Yarkovsky acceleration [10^(-10) au/d^2] |
| `srp` | double precision | Solar radiation pressure [m^2/ton] |
| `a1` | double precision | A1 component of the non-gravitational acceleration for comets [10^(-10) au/d^2] |
| `a2` | double precision | A2 component of the non-gravitational acceleration for comets [10^(-10) au/d^2] |
| `a3` | double precision | A3 component of the non-gravitational acceleration for comets [10^(-10) au/d^2] |
| `dt` | double precision | DeltaT component of the non-gravitational acceleration [days] |
| `mean_anomaly` | double precision | Mean anomaly [degrees] |
| `period` | double precision | Orbital period [days] |
| `mean_motion` | double precision | Orbital mean motion [degrees per day] |
| `a_unc` | double precision | Post-fit 1-sigma uncertainty in the semi-major axis [au] |
| `q_unc` | double precision | Post-fit 1-sigma uncertainty in the perihelion distance [au] |
| `e_unc` | double precision | Post-fit 1-sigma uncertainty in the eccentricity |
| `i_unc` | double precision | Post-fit 1-sigma uncertainty in the inclination [degrees] |
| `node_unc` | double precision | Post-fit 1-sigma uncertainty in the longitude of the node [degrees] |
| `argperi_unc` | double precision | Post-fit 1-sigma uncertainty in the argument of the pericenter [degrees] |
| `peri_time_unc` | double precision | Post-fit 1-sigma uncertainty in the time of the pericenter passage [days] |
| `yarkovsky_unc` | double precision | Post-fit 1-sigma uncertainty in the A2 component of the Yarkovsky acceleration [10^(-10) au/d^2] |
| `srp_unc` | double precision | Post-fit 1-sigma uncertainty in the solar radiation pressure [m^2/ton] |
| `a1_unc` | double precision | Post-fit 1-sigma uncertainty in the A1 component of the non-gravitational acceleration [10^(-10) au/d^2] |
| `a2_unc` | double precision | Post-fit 1-sigma uncertainty in the A2 component of the non-gravitational acceleration [10^(-10) au/d^2] |
| `a3_unc` | double precision | Post-fit 1-sigma uncertainty in the A3 component of the non-gravitational acceleration [10^(-10) au/d^2] |
| `dt_unc` | double precision | Post-fit 1-sigma uncertainty in the DeltaT component of the non-gravitational acceleration [days] |
| `mean_anomaly_unc` | double precision | Post-fit 1-sigma uncertainty in the mean anomaly [degrees] |
| `period_unc` | double precision | Post-fit 1-sigma uncertainty in the orbital period [days] |
| `mean_motion_unc` | double precision | Post-fit 1-sigma uncertainty in the mean motion [degrees] |
| `epoch_mjd` | double precision | Orbit epoch [TT, MJD] |
| `h` | double precision | Absolute magnitude as computed by OrbFit |
| `g` | double precision | Slope parameter |
| `not_normalized_rms` | double precision | Not normalized post-fit RMS [arcseconds] |
| `normalized_rms` | double precision | Normalized post-fit RMS |
| `earth_moid` | double precision | Minimum Orbit Intersection Distance [au] with respect to the orbit of the Earth. |
| `p_healpix` | bigint | Healpix of the orbits P-Vector |
| `q_healpix` | bigint | Healpix of the orbits Q-Vector |
| `fitting_datetime` | timestamp(6) without time zone | Date and time recorded when the orbital fit was performed |
| `ele255` | text | Orbit encoded in the 255-character ele255 format (mutually exclusive with `ele220`). |
| `parent_body` | text | Name (for planets) or primary designation (permid if relevant, otherwise provid, unpacked). Null if Sun. |
| `u_param_planeto` | integer | Planetocentric MPC defined U parameter. For more information please see https://www.minorplanetcenter.net/iau/info/UValue.html. |
| `a_planeto` | double precision | Planetocentric semi-major axis [au] |
| `a_unc_planeto` | double precision | Post-fit 1-sigma uncertainty in the planetocentric semi-major axis [au] |
| `q_planeto` | double precision | Planetocentric perihelion distance [au] |
| `q_unc_planeto` | double precision | Post-fit 1-sigma uncertainty in the planetocentric perihelion distance [au] |
| `e_planeto` | double precision | Planetocentric eccentricity |
| `e_unc_planeto` | double precision | Post-fit 1-sigma uncertainty in the planetocentric eccentricity |
| `i_planeto` | double precision | Planetocentric inclination [degrees] |
| `i_unc_planeto` | double precision | Post-fit 1-sigma uncertainty in the planetocentric inclination [degrees] |
| `node_planeto` | double precision | Planetocentric longitude of the ascending node [degrees] |
| `node_unc_planeto` | double precision | Post-fit 1-sigma uncertainty in the planetocentric longitude of the ascending node [degrees] |
| `argperi_planeto` | double precision | Planetocentric argument of the pericenter [degrees |
| `argperi_unc_planeto` | double precision | Post-fit 1-sigma uncertainty in the planetocentric argument of the pericenter [degrees |
| `peri_time_planeto` | double precision | Planetocentric time of the passage at the pericenter [days] |
| `peri_time_unc_planeto` | double precision | Post-fit 1-sigma uncertainty in the planetocentric time of the passage at the pericenter [days] |
| `mean_anomaly_planeto` | double precision | Planetocentric mean anomaly [degrees] |
| `mean_anomaly_unc_planeto` | double precision | Post-fit 1-sigma uncertainty in the planetocentric mean anomaly [degrees] |
| `period_planeto` | double precision | Planetocentric orbital period [days] |
| `period_unc_planeto` | double precision | Post-fit 1-sigma uncertainty in the planetocentric orbital period [days] |
| `mean_motion_planeto` | double precision | Planetocentric orbital mean motion [degrees per day] |
| `mean_motion_unc_planeto` | double precision | Post-fit 1-sigma uncertainty in the planetocentric orbital mean motion [degrees per day] |

<!-- END GENERATED SCHEMA TABLE -->

[Back to schema overview](../replicated-tables-schema.md)
