# Schema: primary_objects

The primary objects table contains the primary designations for objects designated by the MPC: minor planets, comets, and natural satellites.

## Useful information

- Both packed and unpacked forms are included for primary provisional designations.
- Comet fragments are not included in this table; they are disseminated through a separate table.
- Although the packed primary designation is available, the MPC strongly recommends using unpacked primary designations in queries.
- For <em>object_type</em>, see the [object types documentation](../../orbits/object-types.md). This value is synchronized with <em>object_type</em> in the [current_identifications table](current-identifications.md) for the corresponding primary designation.
- Every entry in <em>primary_objects</em> must have a corresponding entry in the [current_identifications table](current-identifications.md), and vice versa.
- Objects in <em>primary_objects</em> do not necessarily have associated observations or orbits. The <em>object_type</em> field can help distinguish objects with orbits and/or observations from those without them.
- Some fields are not currently populated because they are not used by the MPC. These fields may be deprecated in the future; if you use them, please [let us know](https://mpc-service.atlassian.net/servicedesk/customer/portals).
- Please [contact the MPC](https://mpc-service.atlassian.net/servicedesk/customer/portals) if you experience any issues with this table.

| Column | Data type | Description | Nullable |
|--------|-----------|-------------|----------|
| id | integer | PostgreSQL automatically generated identifier for row of data | Not Null |
| created_at | timestamp(6) without time zone | Date and time of initial row insert | |
| updated_at | timestamp(6) without time zone | Date and time of latest row update | |
| packed_primary_provisional_designation | text | Packed primary provisional designation (e.g. K17P08M) | Not Null |
| unpacked_primary_provisional_designation | text | Unpacked primary provisional designation (e.g. 2017 PM8) | Not Null |
| object_type | integer | Object type classification | |
| status | integer | Result of orbit fitting (not currently used) | |
| standard_minor_planet | boolean | Whether the orbit is in the standard_minor_planet table (not currently used) | Not Null |
| standard_epoch | boolean | Whether standard-epoch orbit is populated (not currently used) | Not Null |
| orbfit_epoch | boolean | Whether mid-observation epoch orbit is populated (not currently used) | Not Null |
| nongravs | boolean | Whether orbit includes non-gravitational perturbations (not currently used) | Not Null |
| satellite | boolean | Whether the object-orbit is in the satellite table (not currently used because included in the <em>orbit_type</em>) | Not Null |
| comet | boolean | Whether the object-orbit is in the comet table (currently always false because not used) | Not Null |
| barycentric | boolean | Whether the orbit is in a barycentric table (currently not used) | Not Null |
| no_orbit | boolean | True if no orbit could be computed (not currently used, already included in the <em>object_type</em>) | Not Null |
| orbit_publication_references | text[] | References to MPC publications containing this orbit (DOU, MPEC, mid-month, Monthly-MPC, etc.) (not currently used) | |
| flag_all_object_obs_consistent | boolean | All observations checked for consistency (not currently used) | Not Null |
| flag_orbit_calculated_from_consistent_obs | boolean | Orbit from flagged-consistent observations (not currently used) | Not Null |
| flag_allowed_external | boolean | Flag to allow orbits to be published (not currently used) | Not Null |
| orbit_published | integer | 0=unpublished, 1=MPEC, 2=DOU, 3=mid-month, 4=monthly | |

[Back to schema overview](../replicated-tables-schema.md)
