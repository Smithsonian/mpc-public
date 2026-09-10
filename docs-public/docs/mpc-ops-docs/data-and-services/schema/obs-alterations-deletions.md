# Schema: obs_alterations_deletions

The observations alterations deletions table records observations that were published (in an MPEC, DOU, or circular) and subsequently deleted. Once deleted, observations disappear from the `obs_sbn` table.

!!! note
    The table alone cannot reproduce all different deletion files published daily (e.g. `todelete.dat`, `removed_obs.dat`).

<!-- BEGIN GENERATED SCHEMA TABLE — managed by generate_public_schema_docs.py; do not edit below by hand -->

## Columns

| Column | Data type | Description |
|--------|-----------|-------------|
| `id` | integer | PostgreSQL automatically generated identifier |
| `obsid` | text | Unique MPC assigned observation ID (in the obs_sbn table) of the deleted observation |
| `publication_ref` | text[] | Array of references to the publications announcing the deletion |
| `status` | integer | Integer describing the publication status: 0=Unpublished (waiting for publication), 1=Published in the DOU, 2=Published in the Monthy Circular |
| `created_at` | timestamp without time zone | Date and time of initial row insert |
| `updated_at` | timestamp without time zone | Date and time of latest row update |

<!-- END GENERATED SCHEMA TABLE -->

[Back to schema overview](../replicated-tables-schema.md)
