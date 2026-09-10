# Schema: obs_alterations_unassociations

The observations alterations unassociations table records observations that were unassociated from their current designations. These observations are generally sent to the ITF (Isolated Tracklet File).

!!! note
    When observations are sent to the ITF, the `status` field in `obs_sbn` changes from `P` to `I`.

<!-- BEGIN GENERATED SCHEMA TABLE — managed by generate_public_schema_docs.py; do not edit below by hand -->

## Columns

| Column | Data type | Description |
|--------|-----------|-------------|
| `id` | integer | PostgreSQL automatically generated identifier |
| `obsid` | text | Unique MPC assigned observation ID (in the obs_sbn table) of the deleted observation |
| `unpacked_provisional_designation_from` | text | Previous unpacked provisional designation (for information on the unpacked provisional designation see https://minorplanetcenter.net/mpcops/documentation/provisional-designation-definition/#unpacked_provid) |
| `packed_provisional_designation_from` | text | Previous packed provisional designation (for information on the unpacked provisional designation see https://minorplanetcenter.net/mpcops/documentation/provisional-designation-definition/#packed_provid) |
| `trkmpc_to` | text | New MPC object identifier used to label the observations in the ITF (for information on the ITF, please see https://minorplanetcenter.net/mpcops/documentation/identifications/) |
| `publication_ref` | text[] | Array of references to the publications announcing the unassociation |
| `created_at` | timestamp without time zone | Date and time of initial row insert |
| `updated_at` | timestamp without time zone | Date and time of latest row update |

<!-- END GENERATED SCHEMA TABLE -->

[Back to schema overview](../replicated-tables-schema.md)
