# Schema: obs_alterations_redesignations

The observations alterations redesignations table records observations that have been redesignated -- tracklets officially published in MPC circulars that have now been assigned a brand new designation.

!!! note
    - Usually published in a monthly circular; recorded in `redesigs.dat` in the meantime.
    - MPC is drastically reducing redesignations; this table may be used less in the future.

<!-- BEGIN GENERATED SCHEMA TABLE — managed by generate_public_schema_docs.py; do not edit below by hand -->

## Columns

| Column | Data type | Description |
|--------|-----------|-------------|
| `id` | integer | PostgreSQL automatically generated identifier |
| `obsid` | text | Unique MPC assigned observation ID (in the obs_sbn table) of the deleted observation |
| `packed_provisional_designation_from` | text | Previous packed provisional designation (for information on the unpacked provisional designation see https://minorplanetcenter.net/mpcops/documentation/provisional-designation-definition/#packed_provid) |
| `unpacked_provisional_designation_from` | text | Previous unpacked provisional designation (for information on the unpacked provisional designation see https://minorplanetcenter.net/mpcops/documentation/provisional-designation-definition/#unpacked_provid) |
| `packed_provisional_designation_to` | text | New packed provisional designation (for information on the unpacked provisional designation see https://minorplanetcenter.net/mpcops/documentation/provisional-designation-definition/#packed_provid) |
| `unpacked_provisional_designation_to` | text | New unpacked provisional designation (for information on the unpacked provisional designation see https://minorplanetcenter.net/mpcops/documentation/provisional-designation-definition/#unpacked_provid) |
| `publication_ref` | text[] | Array of references to the publications announcing the redesignation |
| `status` | integer | Integer describing the publication status: 0=Unpublished (waiting for publication), 1=Published in the DOU, 2=Published in the Monthy Circular |
| `created_at` | timestamp without time zone | Date and time of initial row insert |
| `updated_at` | timestamp without time zone | Date and time of latest row update |
| `new_designation_created` | boolean | Boolean to indicate whether a new designation was created as a result of the redesignations: True=a new designation was created, False=the tracklets were associated to an already existing object |

<!-- END GENERATED SCHEMA TABLE -->

[Back to schema overview](../replicated-tables-schema.md)
