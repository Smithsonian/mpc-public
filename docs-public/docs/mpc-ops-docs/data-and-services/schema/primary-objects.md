# Schema: primary_objects

The primary objects table contains all objects designated by the MPC: minor planets, comets, and natural satellites.

## Useful information

- Both packed and unpacked forms are included for primary provisional designations.
- Some fields are not being currently populated.

<!-- BEGIN GENERATED SCHEMA TABLE — managed by generate_public_schema_docs.py; do not edit below by hand -->

## Columns

| Column | Data type | Description |
|--------|-----------|-------------|
| `id` | integer | PostgreSQL automatically generated identifier |
| `packed_primary_provisional_designation` | text | Packed form of the primary provisional designation (e.g. K17P08M) |
| `unpacked_primary_provisional_designation` | text | Unpacked form of the primary provisional designation (e.g. 2017 PM8) |
| `status` | integer | Result of the orbit fitting. This is still not used |
| `standard_minor_planet` | boolean | Boolean to indicate whether the orbit of the object is specified in the standard_minor_planet table. This is not used right now, but we might use it in the future |
| `standard_epoch` | boolean | If the object is in the standard_minor_planet table, this boolean indicates whether an orbit at the standard-epoch is populated |
| `orbfit_epoch` | boolean | If the object is in the standard_minor_planet table, this boolean indicates whether the orbit at the mid-observation epoch is populated |
| `nongravs` | boolean | Boolean to indicate whether the orbit of the object is specified in the table containing orbits with nongravitational perturbations. At the moment this is not used because we do not have a table for the orbits computed including nongravitational perturbations, even though we compute them. We might use this flag in the future it to indicate whether we computed the orbit of the object using non-gravitational perturbations. |
| `satellite` | boolean | Boolean to indicate whether the object-orbit is specified in the satellite table |
| `comet` | boolean | Boolean to indicate whether the object-orbit is specified in the comet table. The values are currently false because we are not saving comet orbits in a comet table |
| `barycentric` | boolean | Boolean to indicate whether the orbit for the object is in a barycentric table. The values for this field are always false because we are not computing barycentric orbits. |
| `no_orbit` | boolean | Flag to indicate those cases for which it was not possible to compute an orbit. |
| `orbit_publication_references` | text[] | Array of references to MPC publication(s) containing this particular orbit calculation (e.g. DOU MPEC, mid-month, Monthly-MPC, etc) |
| `flag_all_object_obs_consistent` | boolean | Flag to indicate if all observations for an object have been checked to be consistent with obs files. We are not currently using this field. |
| `flag_orbit_calculated_from_consistent_obs` | boolean | Flag to indicate if the the orbit was calculated using the observations flagged as consistent. This flag is not used |
| `flag_allowed_external` | boolean | Flag to indicate if the orbit has been computed using all the observations available and if the observations were consisten with the flat files. This flat is not used. |
| `created_at` | timestamp without time zone | Date and time of initial row insert |
| `updated_at` | timestamp without time zone | Date and time of latest row update |
| `orbit_published` | integer | Flag indicating if the orbit has been published in a Circular. Field values are: 0=unpublished ; 1=published as MPEC; 2=published in DOU ; 3=published in mid-month ; 4=published in monthly. Please note that we are talking about orbit publication and not object designations |
| `object_type` | integer | Integer to indicate the object type as defined in: https://minorplanetcenter.net/mpcops/documentation/object-types/ |

<!-- END GENERATED SCHEMA TABLE -->

[Back to schema overview](../replicated-tables-schema.md)
