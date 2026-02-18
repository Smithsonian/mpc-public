# Schema: primary_objects

The primary objects table contains all objects designated by the MPC: minor planets, comets, and natural satellites.

## Useful information

- Both packed and unpacked forms are included for primary provisional designations.
- Some fields are not being currently populated.

| Column | Data type | Description |
|--------|-----------|-------------|
| orbit_publication_references | text[] | References to MPC publications containing this orbit (DOU, MPEC, mid-month, Monthly-MPC, etc.) |
| comet | boolean | Whether the object-orbit is in the comet table (currently always false) |
| satellite | boolean | Whether the object-orbit is in the satellite table |
| barycentric | boolean | Whether the orbit is in a barycentric table (always false) |
| standard_minor_planet | boolean | Whether the orbit is in the standard_minor_planet table (not currently used) |
| nongravs | boolean | Whether orbit includes non-gravitational perturbations (not currently used) |
| created_at | timestamp(6) without time zone | Date and time of initial row insert |
| updated_at | timestamp(6) without time zone | Date and time of latest row update |
| orbit_published | integer | 0=unpublished, 1=MPEC, 2=DOU, 3=mid-month, 4=monthly |
| flag_all_object_obs_consistent | boolean | All observations checked for consistency (not currently used) |
| flag_allowed_external | boolean | Orbit computed with all available/consistent observations (not used) |
| flag_orbit_calculated_from_consistent_obs | boolean | Orbit from flagged-consistent observations (not used) |
| no_orbit | boolean | True if no orbit could be computed |
| standard_epoch | boolean | Whether standard-epoch orbit is populated |
| orbfit_epoch | boolean | Whether mid-observation epoch orbit is populated |
| object_type | integer | Object type classification |
| packed_primary_provisional_designation | text | Packed primary provisional designation (e.g. K17P08M) |
| id | integer | PostgreSQL automatically generated identifier for row of data |
| status | integer | Result of orbit fitting (not currently used) |
| unpacked_primary_provisional_designation | text | Unpacked primary provisional designation (e.g. 2017 PM8) |

[Back to schema overview](../replicated-tables-schema.md)
