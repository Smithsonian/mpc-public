# Schema: obs_alterations_corrections

The observations alterations corrections table records corrections made to published observations.

!!! warning
    The table is currently empty and the schema may change. Remeasurements are still a work in progress.

<!-- BEGIN GENERATED SCHEMA TABLE — managed by generate_public_schema_docs.py; do not edit below by hand -->

## Columns

| Column | Data type | Description |
|--------|-----------|-------------|
| `id` | integer | PostgreSQL automatically generated identifier |
| `obsid_old` | text | Unique MPC assigned observation ID (in the obs_sbn table) of the wrong observation that was replaced |
| `obsid_new` | text | Unique MPC assigned observation ID (in the obs_sbn table) of the new corrected observation |
| `publication_ref` | text[] | Array of references to the publications announcing the correction |
| `created_at` | timestamp without time zone | Date and time of initial row insert |
| `updated_at` | timestamp without time zone | Date and time of latest row update |

<!-- END GENERATED SCHEMA TABLE -->

[Back to schema overview](../replicated-tables-schema.md)
