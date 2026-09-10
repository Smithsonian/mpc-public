# Schema: neocp_prev_des

The previous NEOCP objects table contains a list of objects previously listed on the NEOCP, their designation if designated, and the reasons for their removal.

<!-- BEGIN GENERATED SCHEMA TABLE — managed by generate_public_schema_docs.py; do not edit below by hand -->

## Columns

| Column | Data type | Description |
|--------|-----------|-------------|
| `id` | integer | PostgreSQL automatically generated identifier |
| `desig` | text | Observer-assigned object identifier, unique within a submission batch. It could have been altered by the MPC if linking has been performed between NEOCP objects. |
| `status` | text | Reasons for removal (see https://minorplanetcenter.net/mpcops/documentation/neocp-prev-des-removal/) |
| `iau_desig` | text | Unpacked provisional designation, as specified by the IAU (for more information see https://minorplanetcenter.net/mpcops/documentation/provisional-designation-definition/#unpacked_provid) |
| `pkd_desig` | text | Extended packed provisional designation (for more information see https://minorplanetcenter.net/mpcops/documentation/provisional-designation-definition/#extended_packed_provid) |
| `ref` | text | MPEC reference (see https://minorplanetcenter.net/iau/info/References.html) |
| `digest2` | numeric | Digest2 score. For more information see https://ui.adsabs.harvard.edu/abs/2019PASP..131f4501K/abstract and https://ui.adsabs.harvard.edu/abs/2023PASP..135j4505V/abstract |
| `created_at` | timestamp without time zone | Date and time of initial row insert |
| `updated_at` | timestamp without time zone | Date and time of latest row update |

<!-- END GENERATED SCHEMA TABLE -->

[Back to schema overview](../replicated-tables-schema.md)
